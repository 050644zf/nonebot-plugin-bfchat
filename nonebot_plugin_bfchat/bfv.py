from nonebot import get_driver


from nonebot import on_command
from nonebot.params import CommandArg, Depends, _command_arg
from nonebot.adapters.onebot.v11 import GROUP, Message, MessageEvent, MessageSegment, GroupMessageEvent
from nonebot.typing import T_State


import requests
import json

from nonebot_plugin_htmlrender import md_to_pic, html_to_pic

from pathlib import Path

import time

from .config import Config
from .template import apply_template, get_vehicles_data_md, get_weapons_data_md, get_group_list, get_server_md
from .utils import PREFIX, BFV_PLAYERS_DATA, CODE_FOLDER, request_API

GAME = 'bfv'
LANG = 'zh-cn'

def get_player_data(player_name:str)->dict:
    return request_API(GAME,'all',{'name':player_name,'lang':LANG})

def get_server_data(server_name:str)->dict:
    return request_API(GAME,'servers',{'name':server_name,'lang':LANG,"platform":"pc","limit":20})


BFV_BIND = on_command(f'{PREFIX}bfv bind', block=True, priority=1)

BFV_LS = on_command(f'{PREFIX}bfv list', block=True, priority=1)

BFV_SERVER = on_command(f'{PREFIX}bfv server', block=True, priority=1)

BFVF = on_command(f'{PREFIX}bfv', block=True, priority=1)




@BFV_BIND.handle()
async def bfv_binding(event:GroupMessageEvent, state:T_State):
    message = _command_arg(state) or event.get_message()
    player = message.extract_plain_text().strip()
    user = event.get_user_id()
    session = event.group_id
    try:
        result = get_player_data(player)
    except:
        await BFV_BIND.send('无法获取到玩家数据，请检查玩家id是否正确。')
        return
    
    result['__update_time'] = time.time()
    try:
        with open(BFV_PLAYERS_DATA/f'{session}'/f'{user}.json','w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        
        await BFV_BIND.send(f'已绑定玩家id {player}，输入"{PREFIX}bfv me"可查看战绩。')
    except FileNotFoundError:
        await BFVF.send(f'该群未初始化bfv me功能，请联系管理员使用{PREFIX}bf init 初始化')

@BFV_LS.handle()
async def bfv_ls(event:GroupMessageEvent, state:T_State):
    message = _command_arg(state) or event.get_message()
    session = event.group_id
    dlist = []
    for fp in (BFV_PLAYERS_DATA/f'{session}').iterdir():
        with open(fp,encoding='utf-8') as f:
            dlist.append(json.load(f))

    md_result = f"""# 本群已绑定战地五玩家数据

按等级排序

{get_group_list(dlist)}"""

    pic = await md_to_pic(md_result, css_path=CODE_FOLDER/"github-markdown-dark.css",width=700)
    await BFVF.send(MessageSegment.image(pic))
    
@BFV_SERVER.handle()
async def bfv_server(event:MessageEvent, state:T_State):
    message = _command_arg(state) or event.get_message()
    server_name = message.extract_plain_text().strip()
    server_data = get_server_data(server_name)

    md_result = f"""# 搜索服务器：{server_name}
已找到符合要求的服务器 {len(server_data['servers'])} 个，最多显示20个
{get_server_md(server_data)}"""

    pic = await md_to_pic(md_result, css_path=CODE_FOLDER/"github-markdown-dark.css",width=700)
    await BFVF.send(MessageSegment.image(pic))




@BFVF.handle()
async def bfv_handler(event:MessageEvent, state:T_State):
    message = _command_arg(state) or event.get_message()
    args = message.extract_plain_text().strip().split(' ')
    player = args[0]
    if player == 'me' and isinstance(event, GroupMessageEvent):
        user = event.get_user_id()
        session = event.group_id
        try:
            with open(BFV_PLAYERS_DATA/f'{session}'/f'{user}.json','r', encoding='utf-8') as f:
                result = json.load(f)
        except FileNotFoundError:
            if (BFV_PLAYERS_DATA/f'{session}').exists():
                await BFVF.send(f'未找到绑定玩家数据，请使用"{PREFIX}bfv bind [玩家id]"进行绑定')
            else:
                await BFVF.send(f'该群未初始化bfv me功能，请联系管理员使用{PREFIX}bf init 初始化')
            return

        
        player = result['userName']
        if time.time() - result['__update_time'] > 3600:
            result = get_player_data(player)
            result['__update_time'] = time.time()
            with open(BFV_PLAYERS_DATA/f'{session}'/f'{user}.json','w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4) 
    else:
        result = get_player_data(player)
        result['__update_time'] = time.time()



    if len(args)==1:
        html = apply_template(result,'bfv', PREFIX)
        pic = await html_to_pic(html, viewport={"width": 700,"height":10})
        # md_result = mdtemplate(result)
        # print(md_result)
    elif args[1] == 'weapons':
        md_result = f"""## {player} 武器数据

仅展示击杀数前50数据

{get_weapons_data_md(result,50)}"""
        pic = await md_to_pic(md_result, css_path=CODE_FOLDER/"github-markdown-dark.css",width=700)
    elif args[1] == 'vehicles':
        md_result = f"""## {player} 载具数据

仅展示击杀数前50数据

{get_vehicles_data_md(result,50)}"""        


        pic = await md_to_pic(md_result, css_path=CODE_FOLDER/"github-markdown-dark.css",width=700)
    

    await BFVF.send(MessageSegment.image(pic))