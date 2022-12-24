# nonebot-plugin-bfchat

一个基于nonebot2平台的战地1/5聊天机器人，提供战绩查询，群账号绑定，服务器查询等功能，提供基于[htmlrender插件](https://github.com/kexue-z/nonebot-plugin-htmlrender)渲染的美观输出。

## 安装

pip:

```bash
pip install nonebot-plugin-bfchat
```

nb-cli:

```bash
nb plugin install nonebot-plugin-bfchat
```

## 配置项及默认值

```properties
bfchat_prefix = "/"    # bfchat的命令前缀，默认为"/"
bfchat_dir = "./bfchat_data"    # bfchat的存储目录，用于存储群绑定玩家数据
```

## 命令列表

使用以下命令前均需要添加配置好的前缀

| 命令                                                      | 作用                                                                                                   | 备注                                                                         |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------- |
| `bf help`                                               | 返回帮助文档                                                                                           |                                                                              |
| `bf init`                                               | 初始化本群绑定功能，未初始化的群，群员不能使用绑定功能                                                 | 仅SUPERUSER和群管理员有效                                                    |
| `bf1 [玩家id]`<br />`bfv [玩家id]`                    | 查询 `[玩家id]`的bf1/bfv战绩信息                                                                     | 如果查询玩家是me，则会将数据保存至本地<br />且一小时内再次查询不会再发起请求 |
| `bf1 [玩家id] weapons`<br />`bfv [玩家id] weapons`   | 查询 `[玩家id]`的bf1/bfv武器信息                                                                     |                                                                              |
| `bf1 [玩家id] vehicles`<br />`bfv [玩家id] vehicles` | 查询 `[玩家id]`的bf1/bfv载具信息                                                                     |                                                                              |
| `bf1 bind [玩家id]`<br />`bfv bind [玩家id]`          | 将 对应游戏的 `[玩家id]`与命令发送人绑定，绑定后可使用 `me `代替 `[玩家id]`<br />例如 `bfv me` | bf1与bfv绑定不互通                                                           |
| `bf1 list`<br />`bfv list`                            | 列出该服务器所有已绑定的bf1/bfv玩家信息                                                                | 使用本地数据，不会自动更新                                                   |
| `bf1 server [服务器名]`<br />`bfv server [服务器名]`  | 查询名字包含 `[服务器名]`的bf1/bfv服务器                                                             |                                                                              |
