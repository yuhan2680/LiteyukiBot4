---
title: 答疑
icon: object-group
order: 3
category: 使用指南
tag:
  - 配置
  - 部署
---

### 常见问题

- 设备上Python环境太乱了，pip和python不对应怎么办？
    - 请使用`/path/to/python -m pip install -r requirements.txt`来安装依赖，
      然后用`/path/to/python main.py`来启动Bot，
      其中`/path/to/python`是你要用来运行Bot的可执行文件
- 为什么我启动后机器人没有反应？
    - 请检查配置文件的`command_start`或`superusers`，确认你有权限使用命令并按照正确的命令发送

- 怎么登录聊天平台，例如QQ
    - 你有这个问题说明你不是很了解这个项目，本项目不负责实现登录功能，只负责处理和回应消息，登录功能由实现端（协议端）提供，
      实现端本身不负责处理响应逻辑，将消息按照OneBot标准处理好上报给轻雪
      你需要使用Onebot标准的实现端来连接到轻雪并将消息上报给轻雪，下面已经列出一些推荐的实现端

#### 推荐方案(QQ)

1. [Lagrange.OneBot](https://github.com/KonataDev/Lagrange.Core)，目前Markdown点按交互目前仅支持Lagrange
2. [LiteLoaderNTQQ+LLOneBot](https://github.com/LLOneBot/LLOneBot)，基于NTQQ的Onebot实现
3. 云崽的`icqq-plugin`和`ws-plugin`进行通信
4. `Go-cqhttp`（目前已经半死不活了）
5. 人工实现的`Onebot`协议，自己整一个WebSocket客户端，看着QQ的消息，然后给轻雪传输数据

#### 推荐方案(Minecraft)

1. 我们有专门为Minecraft开发的服务器Bot，支持OnebotV11/12标准，详细请看[MinecraftOneBot](https://github.com/snowykami/MinecraftOnebot)

使用其他项目连接请先自行查阅文档，若有困难请联系对应开发者而不是Liteyuki的开发者