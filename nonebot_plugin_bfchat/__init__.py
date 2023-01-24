from nonebot import get_driver


from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import CommandArg, Depends, _command_arg
from nonebot.adapters.onebot.v11 import GROUP, Message, MessageEvent, MessageSegment, GroupMessageEvent
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER


from nonebot_plugin_htmlrender import md_to_pic, html_to_pic

from pathlib import Path

from .utils import PREFIX, BF1_PLAYERS_DATA, BFV_PLAYERS_DATA, BF2042_PLAYERS_DATA, CODE_FOLDER

from .bf1 import bf1_binding, bf1_handler, bf1_ls, bf1_server
from .bfv import bfv_binding, bfv_handler, bfv_ls, bfv_server
from .bf2042 import bf2042_binding, bf2042_handler, bf2042_ls


BF_INIT = on_command(f'{PREFIX}bf init', block=True, priority=1, permission=GROUP_OWNER | GROUP_ADMIN | SUPERUSER)
BF_HELP = on_command(f"{PREFIX}bf help", block=True, priority=1)

@BF_INIT.handle()
async def bf_init(event:MessageEvent, state:T_State):
    if isinstance(event,GroupMessageEvent):
        session = event.group_id
        try:
            (BFV_PLAYERS_DATA/f'{session}').mkdir(exist_ok=True)
            (BF1_PLAYERS_DATA/f'{session}').mkdir(exist_ok=True)
            (BF2042_PLAYERS_DATA/f'{session}').mkdir(exist_ok=True)
            await BF_INIT.send(f'初始化本群绑定功能成功！\n\n群员使用 {PREFIX}bf1 bind [玩家id] 可绑定战地一账号到本群。\n群员使用 {PREFIX}bfv bind [玩家id] 可绑定战地五账号到本群。\n群员使用 {PREFIX}bf2042 bind [玩家id] 可绑定战地2042账号到本群。（测试中）\n绑定后使用{PREFIX}bf1 me 或 {PREFIX}bfv me 或 {PREFIX}bf2042 me 可查询战绩')
        except FileExistsError:
            await BF_INIT.send(f'本群已初始化绑定功能。\n\n群员使用 {PREFIX}bf1 bind [玩家id] 可绑定战地一账号到本群。\n群员使用 {PREFIX}bfv bind [玩家id] 可绑定战地五账号到本群。\n群员使用 {PREFIX}bf2042 bind [玩家id] 可绑定战地2042账号到本群。（测试中）\n绑定后使用{PREFIX}bf1 me 或 {PREFIX}bfv me 或 {PREFIX}bf2042 me 可查询战绩')

@BF_HELP.handle()
async def bf_help(event:MessageEvent, state:T_State):
    with open(CODE_FOLDER/'help.md',encoding='utf-8') as f:
        md_help = f.read()
    
    md_help = md_help.format(p=PREFIX)

    pic = await md_to_pic(md_help, css_path=CODE_FOLDER/"github-markdown-dark.css",width=1200)

    await BF_HELP.send(MessageSegment.image(pic))

all = [
    "bf1_binding", "bf1_handler", "bf1_ls", "bf1_server",
    "bfv_binding", "bfv_handler", "bfv_ls", "bfv_server",
    "bf2042_binding", "bf2042_handler", "bf2042_ls"
]
















