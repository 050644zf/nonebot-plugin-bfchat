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
from .template import apply_template, get_vehicles_data_md, get_weapons_data_md, get_group_list, get_server_md, \
    get_classes_data_md
from .utils import PREFIX, BF2042_PLAYERS_DATA, CODE_FOLDER, request_API

GAME = 'bf2042'
LANG = 'zh-cn'


def get_player_data(player_name: str) -> dict:
    res = request_API(GAME, 'stats', {'name': player_name})
    return res


BF2042_BIND = on_command(f'{PREFIX}bf2042 bind', block=True, priority=1)

BF2042_LS = on_command(f'{PREFIX}bf2042 list', block=True, priority=1)

BF2042F = on_command(f'{PREFIX}bf2042', block=True, priority=1)


@BF2042_BIND.handle()
async def bf2042_binding(event: GroupMessageEvent, state: T_State):
    message = _command_arg(state) or event.get_message()
    player = message.extract_plain_text().strip()
    user = event.get_user_id()
    session = event.group_id
    try:
        result = get_player_data(player)
    except:
        await BF2042_BIND.send('无法获取到玩家数据，请检查玩家id是否正确。')
        return

    result['__update_time'] = time.time()
    try:
        with open(BF2042_PLAYERS_DATA / f'{session}' / f'{user}.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        await BF2042_BIND.send(f'已绑定玩家id {player}，输入"{PREFIX}bf2042 me"可查看战绩。')
    except FileNotFoundError:
        await BF2042F.send(f'该群未初始化bf2042 me功能，请联系管理员使用{PREFIX}bf init 初始化')


@BF2042_LS.handle()
async def bf2042_ls(event: GroupMessageEvent, state: T_State):
    message = _command_arg(state) or event.get_message()
    session = event.group_id
    dlist = []
    for fp in (BF2042_PLAYERS_DATA / f'{session}').iterdir():
        with open(fp, encoding='utf-8') as f:
            dlist.append(json.load(f))

    md_result = f"""# 本群已绑定战地2042玩家数据

按等级排序

{get_group_list(dlist)}"""

    pic = await md_to_pic(md_result, css_path=CODE_FOLDER / "github-markdown-dark.css", width=700)
    await BF2042F.send(MessageSegment.image(pic))


@BF2042F.handle()
async def bf2042_handler(event: MessageEvent, state: T_State):
    message = _command_arg(state) or event.get_message()
    args = message.extract_plain_text().strip().split(' ')
    player = args[0]
    if player == 'me' and isinstance(event, GroupMessageEvent):
        user = event.get_user_id()
        session = event.group_id
        try:
            with open(BF2042_PLAYERS_DATA / f'{session}' / f'{user}.json', 'r', encoding='utf-8') as f:
                result = json.load(f)
        except FileNotFoundError:
            if (BF2042_PLAYERS_DATA / f'{session}').exists():
                await BF2042F.send(f'未找到绑定玩家数据，请使用"{PREFIX}bf2042 bind [玩家id]"进行绑定')
            else:
                await BF2042F.send(f'该群未初始化bf2042 me功能，请联系管理员使用{PREFIX}bf init 初始化')
            return

        player = result['userName']
        if time.time() - result['__update_time'] > 3600:
            result = get_player_data(player)
            result['__update_time'] = time.time()
            with open(BF2042_PLAYERS_DATA / f'{session}' / f'{user}.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
    else:
        result = get_player_data(player)
        result['__update_time'] = time.time()

    if len(args) == 1:
        html = apply_template(result, 'bf2042', PREFIX)
        pic = await html_to_pic(html, viewport={"width": 700, "height": 10})
        # md_result = mdtemplate(result)
        # print(md_result)
    elif args[1] == 'weapons':
        md_result = f"""## {player} 武器数据

仅展示击杀数前50数据

{get_weapons_data_md(result, 50)}"""
        pic = await md_to_pic(md_result, css_path=CODE_FOLDER / "github-markdown-dark.css", width=700)
    elif args[1] == 'vehicles':
        md_result = f"""## {player} 载具数据

仅展示击杀数前50数据

{get_vehicles_data_md(result, 50)}"""
        pic = await md_to_pic(md_result, css_path=CODE_FOLDER / "github-markdown-dark.css", width=700)
    elif args[1] == 'classes':
        md_result = f"""## {player} 专家数据

仅展示击杀数前50数据

{get_classes_data_md(result, 50)}"""
        pic = await md_to_pic(md_result, css_path=CODE_FOLDER / "github-markdown-dark.css", width=700)

    await BF2042F.send(MessageSegment.image(pic))
