---
title: Python Wechaty如何使用PadLocal Puppet Service
---

## Python Wechaty如何使用PadLocal Puppet Service

本文描述Python语言下如何使用iPad协议的PadLocal Token。其他Wechaty多语言开发也能做参考。

- [wechaty-puppet-padlocal](https://github.com/padlocal/wechaty-puppet-padlocal)
- [TOKEN 申请方法](https://wechaty.js.org/docs/puppet-services/)

## 搭建PadLocal Token Gateway

```shell
# 设置环境变量

export WECHATY_LOG="verbose"
export WECHATY_PUPPET="wechaty-puppet-padlocal"
export WECHATY_PUPPET_PADLOCAL_TOKEN="puppet_padlocal_XXXXXX"

export WECHATY_PUPPET_SERVER_PORT="9001"
export WECHATY_TOKEN="1fe5f846-3cfb-401d-b20c-XXXXX"

docker run -ti \
  --name wechaty_puppet_service_token_gateway \
  --rm \
  -e WECHATY_LOG \
  -e WECHATY_PUPPET \
  -e WECHATY_PUPPET_PADLOCAL_TOKEN \
  -e WECHATY_PUPPET_SERVER_PORT \
  -e WECHATY_TOKEN \
  -p "$WECHATY_PUPPET_SERVER_PORT:$WECHATY_PUPPET_SERVER_PORT" \
  wechaty/wechaty:0.56
```

- WECHATY_PUPPET_PADLOCAL_TOKEN 申请得到的token代码
- WECHATY_PUPPET_SERVER_PORT 设置对外访问端口，需要保证端口没被占用，没被防火墙匹配
- WECHATY_TOKEN 生成个人随机[TOKEN](https://www.uuidgenerator.net/version4)。WECHATY_TOKEN：个人理解为和远程wechaty服务器做通讯用，通过这个唯一token可以返回当前主机访问地址和端口。所以需要避免和别人重复。

可以通过下面代码，确定是否成功。

```shell
curl https://api.chatie.io/v0/hosties/$WECHATY_TOKEN (个人随机token)
{"ip":"36.7.XXX.XXX","port":9001}
```

## python-Wechaty对接GateWay

在对接Gateway的时候，这里需要注意下，如果GateWay是部署在公网可以访问的服务器上，按照默认配置就可访问；如果是部署在自己内网服务器上，就会报`Your service token has no available endpoint, is your token correct?`，这个时候需要设置WECHATY_PUPPET_SERVICE_ENDPOINT。

```shell
#1  默认配置
export WECHATY_PUPPET="wechaty-puppet-service"
export WECHATY_PUPPET_SERVICE_TOKEN="1fe5f846-3cfb-401d-b20c-XXXXX"

#2  主机是部署在内网服务器上
export WECHATY_PUPPET="wechaty-puppet-service"
export WECHATY_PUPPET_SERVICE_TOKEN="1fe5f846-3cfb-401d-b20c-XXXXX"
export WECHATY_PUPPET_SERVICE_ENDPOINT="192.168.1.56:9001"
```

WECHATY_PUPPET_SERVICE_ENDPOINT：内网IP地址:端口号

### python-wechaty-getting-started

```shell
git clone https://github.com/wj-Mcat/python-wechaty-getting-started
cd python-wechaty-getting-started

export WECHATY_PUPPET="wechaty-puppet-service"
export WECHATY_PUPPET_SERVICE_TOKEN="1fe5f846-3cfb-401d-b20c-XXXXX"

python examples/ding-dong-bot.py
```

到此，恭喜你入坑。
具体的使用可以查看[python-wechaty-getting-started](https://github.com/wechaty/python-wechaty-getting-started)

## 参考

- 如何成为 `Wechaty Contributor` 可以通过该链接查看 [https://wechaty.js.org/docs/contributor-program/](https://wechaty.js.org/docs/contributor-program/)
- [.NET Wechaty 如何使用 PadLocal Puppet Service](https://wechaty.js.org/2021/01/28/csharp-wechaty-for-padlocal-puppet-service/)
- 特别感谢 @huan 的帮助。
