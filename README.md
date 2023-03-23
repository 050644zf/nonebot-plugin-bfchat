<div align="center">xdm, you V ma?</div>

# nonebot-plugin-bfchat

一个基于nonebot2平台的战地1/5/2042(测试中)聊天机器人，提供战绩查询，群账号绑定，服务器查询等功能，提供基于[htmlrender插件](https://github.com/kexue-z/nonebot-plugin-htmlrender)渲染的美观输出。

## 安装

nb-cli: (推荐)

```bash
nb plugin install nonebot-plugin-bfchat
```

pip: (需要在pyproject.toml手动导入)

```bash
pip install nonebot-plugin-bfchat
```

## 配置项及默认值

```properties
bfchat_prefix = "/"    # bfchat的命令前缀，默认为"/"
bfchat_dir = "./bfchat_data"    # bfchat的存储目录，用于存储群绑定玩家数据
```

## 命令列表

使用以下命令前均需要添加配置好的前缀

 将 `[game]` 替换为 `bf1 `, `bfv `, `bf2042` 查询对应游戏。

| 命令                         | 作用                                                                                                   | 备注                                                                         |
| ---------------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| `bf help`                  | 返回本列表                                                                                             |                                                                              |
| `bf init`                  | 初始化本群绑定功能，未初始化的群，群员不能使用绑定功能                                                 | 仅SUPERUSER和群管理员有效                                                    |
| `[game] [玩家id]`          | 查询 `[玩家id]`的战绩信息<br />例如查询 `senpai`的 `bf1`信息：`bf1 senpai`                     | 如果查询玩家是me，则会将数据保存至本地<br />且一小时内再次查询不会再发起请求 |
| `[game] [玩家id] weapons`  | 查询 `[玩家id]`的武器信息                                                                            |                                                                              |
| `[game] [玩家id] vehicles` | 查询 `[玩家id]`的载具信息                                                                            |                                                                              |
| `bf2042 [玩家id] classes`  | 查询 `[玩家id]`的bf2042专家信息                                                                      |                                                                              |
| `[game] bind [玩家id]`     | 将 对应游戏的 `[玩家id]`与命令发送人绑定，绑定后可使用 `me `代替 `[玩家id]`<br />例如 `bfv me` | 游戏间绑定不互通                                                             |
| `[game] list`              | 列出该服务器所有已绑定的bf1/bfv玩家信息                                                                | 使用本地数据，不会自动更新                                                   |
| `[game] server [服务器名]` | 查询名字包含 `[服务器名]`的bf1/bfv服务器                                                             |                                                                              |

## 示例

bfv me

<img src="https://raw.githubusercontent.com/050644zf/nonebot-plugin-bfchat/master/img/bfvme.jpg" width="400px"/>

bfv server BFV ROBOT

![img](https://raw.githubusercontent.com/050644zf/nonebot-plugin-bfchat/master/img/server.png)

bfv list

![img](https://raw.githubusercontent.com/050644zf/nonebot-plugin-bfchat/master/img/bflist.png)
