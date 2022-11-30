## 一、支持的协议

一个Wechaty实例/派生类就是机器人对象，能够根据`TOKEN`找到连接的服务，获取用户自模块执行搜索，而这些信息都是由Wechaty实例管理。

> 由于服务的连接信息是保存到实例当中，故用户子模块一定要通过Wechaty实例来获取。例如：bot.Contact.find_all()

### 1.1 什么是协议

所有实现底层平台对接实现就是一个协议。

python-wechaty理论上能够对接所有IM平台，目前已经对接微信、微信公众号、钉钉、飞书以及WhatsApp等平台，源码都是基于TypeScript语言，可是通过`wechaty-puppet-service`能够将其服务以gRPC的形式暴露出来，提供给多语言`Wechaty`来连接。例如微信免费Web协议，底层实现是基于TyepScript编写，可是通过社区生态项目，可是都可以使用docker将接口的实现部署成服务。

比如[wechaty-puppet-wechat](https://github.com/wechaty/wechaty-puppet-wechat)能够通过[wechaty/wechaty:latest](https://hub.docker.com/r/wechaty/wechaty)镜像将其所有实现接口暴露成gRPC的服务，非常的方便，已然实现`write once, run anywhere`。

### 1.2 协议列表

目前python-wechaty能够使用wechaty生态中所有IM平台对接协议，协议列表如下所示：

* [wechaty-puppet-wechaty](https://github.com/wechaty/wechaty-puppet-wechat): 免费微信Web协议
* [wechaty-puppet-](https://github.com/wechaty/wechaty-puppet-macOS): 免费微信MacOs协议
* [wechaty-puppet-padlocal](https://github.com/wechaty/wechaty-puppet-padlocal): 付费微信Pad协议
* [wechaty-puppet-official-account](https://github.com/wechaty/wechaty-puppet-official-account): 微信公众号协议
* [wechaty-puppet-lark](https://github.com/wechaty/wechaty-puppet-lark): 飞书协议
* [wechaty-puppet-dingtalk](https://github.com/wechaty/wechaty-puppet-dingtalk): 钉钉协议
* [wechaty-puppet-teams](https://github.com/wechaty/wechaty-puppet-dingtalk): 微软Teams协议
* ......


