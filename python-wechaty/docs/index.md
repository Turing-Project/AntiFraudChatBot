# Welcome to python-wechaty

![](./img/getting-started/python-wechaty.png)

## 一、Wechaty 是什么

Wechaty 是一个开源聊天机器人框架SDK，具有高度封装、高可用的特性，支持NodeJs, Python, Go 和Java 等多语言版本。在过去的4年中，服务了数万名开发者，收获了 Github 的 1w+ Star。同时配置了完整的 DevOps 体系并持续按照 Apache 的方式管理技术社区。

目前IM平台众多，为了实现`write once run anlywhere`，Wechaty 将IM平台中通用的消息处理进行高度抽象封装，提供统一的上层接口，让开发者不用关心具体底层实现细节，用简单的代码开发出功能强大的聊天机器人。

## 二、Python-Wechaty 是什么

> 理论上python-wechaty可以对接任何IM平台

python-wechaty是基于Wechaty生态派生出的Python编程语言客户端，能够让开发者使用少量代码对接到各个即时通讯软件平台。在过去的一年里，python-wechaty致力于提升代码鲁棒性、添加社区开箱即用的工具、以及完善软件开发文档。

目前可对接：

- [微信](https://github.com/wechaty/wechaty-puppet-wechat)
- [微信公众号](https://github.com/wechaty/wechaty-puppet-official-account)
- [钉钉](https://github.com/wechaty/wechaty-puppet-dingtalk)
- [飞书](https://github.com/wechaty/wechaty-puppet-lark)
- [WhatsApp](https://github.com/wechaty/wechaty-puppet-whatsapp)
- [Gitter](https://github.com/wechaty/wechaty-puppet-gitter)
- ...

## 三、TOKEN 是什么

如果要开发微信聊天机器人时，wechaty会使用token来连接第三方的服务；如果要开发飞书聊天机器人时，wechaty会使用token和secret来连接官方服务接口；如果要将node puppet以服务的形式部署到服务器上时，自定义的token将会是作为服务连接的钥匙。

![token gateway](./img/introduction/cloud.png)

TOKEN是一个用来连接底层服务的密钥，也是开发聊天机器人的第一步；官网有介绍[如何获取TOKEN](https://wechaty.js.org/docs/puppet-services/#get-a-token)。
