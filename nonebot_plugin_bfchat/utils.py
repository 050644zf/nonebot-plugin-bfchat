import json
import requests
from pathlib import Path

from .config import Config
from nonebot import get_driver

CODE_FOLDER = Path(__file__).parent.resolve()

global_config = get_driver().config
config = Config(**global_config.dict())
PREFIX = config.bfchat_prefix

CURRENT_FOLDER = Path(config.bfchat_dir).resolve()
CURRENT_FOLDER.mkdir(exist_ok=True)
BFV_PLAYERS_DATA = CURRENT_FOLDER/'bfv_players'
BF1_PLAYERS_DATA = CURRENT_FOLDER/'bf1_players'
BF2042_PLAYERS_DATA = CURRENT_FOLDER/'bf2042_players'

BFV_PLAYERS_DATA.mkdir(exist_ok=True)
BF1_PLAYERS_DATA.mkdir(exist_ok=True)
BF2042_PLAYERS_DATA.mkdir(exist_ok=True)

API_SITE = "https://api.gametools.network/"

def request_API(game, prop='stats', params={}):
    url = API_SITE+f'{game}/{prop}'

    res = requests.get(url,params=params)
    if res.status_code == 200:
        return json.loads(res.text)
    else:
        raise requests.HTTPError