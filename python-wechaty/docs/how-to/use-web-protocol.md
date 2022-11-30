---
title: "教你用python-wecahty和web协议开发机器人"
date: 2021-04-25
---

写这篇文章的原因: go-wechaty作者[dchaofei](https://github.com/dchaofei)抢先写了[web协议复活的博客](https://wechaty.js.org/2021/04/16/go-wechaty-use-web/)，作为[python-wechaty](http://github.com/wechaty/python-wechaty)的作者我也需要给大家更加详细的介绍如何使用[python-wechaty](http://github.com/wechaty/python-wechaty)来登陆web版本的微信。

## 一、介绍

微信版本的机器人种类很多，出现的协议也很多，比如Ipad、Mac以及Windows协议，而最早出现的其实是web版本的协议。在前几年由于腾讯的一些限制，将大部分用户的web登陆的权限给关掉了，导致很多web协议版本的微信机器人直接死掉了，比如著名的itchat。

可是自从统信和腾讯共同推出桌面版本的微信之后，web版本的机器人以某种方式复活了，而wechaty便是最早来解决这个事情的开源项目之一，接下来我将详细介绍如何使用[python-wechaty](http://github.com/wechaty/python-wechaty)基于web版本协议开发聊天机器人。

整体步骤分为两步：

* 使用Docker启动web协议服务
* 使用python-wechaty连接服务

第一步将web版本的协议以gRPC服务的形式暴露出来，使用过程非常简单，只是需要注意几个配置项；第二步则是使用python-wechaty连接该服务，开发聊天机器人。

## 二、启动web协议服务

启动web协议服务脚本如下所示：

```shell
docker pull wechaty/wechaty:latest

export WECHATY_LOG="verbose"
export WECHATY_PUPPET="wechaty-puppet-wechat"
export WECHATY_PUPPET_SERVER_PORT="8080"
export WECHATY_TOKEN="python-wechaty-uos-token"
export WECHATY_PUPPET_SERVICE_NO_TLS_INSECURE_SERVER="true"

docker run -ti \
--name wechaty_puppet_service_token_gateway \
--rm \
-e WECHATY_LOG \
-e WECHATY_PUPPET \
-e WECHATY_PUPPET_SERVER_PORT \
-e WECHATY_TOKEN \
-p "$WECHATY_PUPPET_SERVER_PORT:$WECHATY_PUPPET_SERVER_PORT" \
wechaty/wechaty:latest
```

如果是在本地测试时，`WECHATY_PUPPET_SERVER_PORT`和`WECHATY_TOKEN`相对比较随意，大家都可以随时设置，因为下一步中的连接可以设置本地连接。

如果是在服务端部署时，`WECHATY_PUPPET_SERVER_PORT`是需要保证所在服务器的该端口是保持开放的，以保证使用`python-wechaty`能够正常连接；此外`WECHATY_TOKEN`将用于在wechaty token中心注册启动的服务，以让[python-wechaty](http://github.com/wechaty/python-wechaty)能够找到该服务的地址，所以必须是修改成唯一标识符，推荐使用`uuid`来代替`python-wechaty-uos-token`。

## 三、连接服务

使用python开发最简单的聊天机器人，代码如下所示：

```python
# bot.py
from wechaty import Wechaty
import os

import asyncio
async def main():
    bot = Wechaty()
    bot.on('scan', lambda status, qrcode, data: print('Scan QR Code to login: {}\nhttps://wechaty.js.org/qrcode/{}'.format(status, qrcode)))
    bot.on('login', lambda user: print('User {} logged in'.format(user)))
    bot.on('message', lambda message: print('Message: {}'.format(message)))
    await bot.start()

asyncio.run(main())
```

当在本地测试时，可以通过设置`WECHATY_PUPPET_SERVICE_ENDPOINT`环境变量让`python-wechaty`直接与本地的web服务连接。例如：`WECHATY_PUPPET_SERVICE_ENDPOINT=127.0.0.1:8080`，运行脚本如下所示：

```shell
WECHATY_PUPPET_SERVICE_TOKEN=python-wechaty-uos-token WECHATY_PUPPET_SERVICE_ENDPOINT=127.0.0.1:8080 python bot.py
```

当在远端服务器部署时，只需要设置`WECHATY_PUPPET_SERVICE_TOKEN`即可连接启动的web服务，运行脚本如下所示：

```shell
WECHATY_PUPPET_SERVICE_TOKEN=python-wechaty-uos-token python bot.py
```

## 四、总结

python-wechaty是一个非常简单的聊天机器人框架，理论上能够对接任何IM平台，拥有原生与AI对接的能力，能够快速开发出功能强大的Chatbot，欢迎大家关注[python-wechaty](https://github.com/wechaty/python-wechaty)

## 五、相关链接

* [python-wechty](https://github.com/wechaty/python-wechaty)
* [python-wechaty getting started](https://github.com/wechaty/python-wechaty-getting-started )
* [web协议复活](https://wechaty.js.org/2021/04/13/wechaty-uos-web/)
* [Python Wechaty Getting Started](https://wechaty.js.org/docs/polyglot/python/)
* [puppet-providers](https://wechaty.js.org/docs/puppet-providers/wechat)
