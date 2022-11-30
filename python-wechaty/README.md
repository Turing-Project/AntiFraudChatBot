<!-- markdownlint-disable MD033 -->
# python-wechaty

![Python Wechaty](./docs/img/getting-started/python-wechaty.png)

[![PyPI Version](https://img.shields.io/pypi/v/wechaty?color=blue)](https://pypi.org/project/wechaty/)
[![Python Wechaty Getting Started](https://img.shields.io/badge/Python%20Wechaty-Getting%20Started-blue)](https://github.com/wechaty/python-wechaty-getting-started)
[![Python 3.7](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Downloads](https://pepy.tech/badge/wechaty)](https://pepy.tech/project/wechaty)
[![Wechaty in Python](https://img.shields.io/badge/Wechaty-Python-blue)](https://github.com/wechaty/python-wechaty)
[![codecov](https://codecov.io/gh/wechaty/python-wechaty/branch/master/graph/badge.svg)](https://codecov.io/gh/wechaty/python-wechaty)
[![PyPI](https://github.com/wechaty/python-wechaty/actions/workflows/pypi.yml/badge.svg)](https://github.com/wechaty/python-wechaty/actions/workflows/pypi.yml)
![PyPI - Downloads](https://img.shields.io/pypi/dm/wechaty?color=blue)

[📄 Chinese Document](https://wechaty.readthedocs.io/zh_CN/latest/)  [python-wechaty-template](https://github.com/wechaty/python-wechaty-template)

## Getting Started

* [Python Wechaty Quick Start Project Template](https://github.com/wechaty/python-wechaty-template)
* [Padlocal机器人](https://wechaty.readthedocs.io/zh_CN/latest/introduction/use-padlocal-protocol/)
* 钉钉机器人
* 微信公众号机器人
* 飞书机器人
* ...

## Connecting Chatbots

[![Powered by Wechaty](https://img.shields.io/badge/Powered%20By-Wechaty-brightgreen.svg)](https://github.com/Wechaty/wechaty)

Wechaty is a Conversational SDK for Chatbot Makers that can help you create a bot in 9 lines of Python.

## Voice of the Developers

> "Wechaty is a great solution, I believe there would be much more users recognize it." [link](https://github.com/Wechaty/wechaty/pull/310#issuecomment-285574472)  
> &mdash; <cite>@Gcaufy, Tencent Engineer, Author of [WePY](https://github.com/Tencent/wepy)</cite>
>
> "太好用，好用的想哭"  
> &mdash; <cite>@xinbenlv, Google Engineer, Founder of HaoShiYou.org</cite>
>
> "最好的微信开发库" [link](http://weibo.com/3296245513/Ec4iNp9Ld?type=comment)  
> &mdash; <cite>@Jarvis, Baidu Engineer</cite>
>
> "Wechaty让运营人员更多的时间思考如何进行活动策划、留存用户，商业变现" [link](http://mp.weixin.qq.com/s/dWHAj8XtiKG-1fIS5Og79g)  
> &mdash; <cite>@lijiarui, Founder & CEO of Juzi.BOT.</cite>
>
> "If you know js ... try Wechaty, it's easy to use."  
> &mdash; <cite>@Urinx Uri Lee, Author of [WeixinBot(Python)](https://github.com/Urinx/WeixinBot)</cite>

See more at [Wiki:Voice Of Developer](https://github.com/Wechaty/wechaty/wiki/Voice%20Of%20Developer)

## Join Us

Wechaty is used in many ChatBot projects by thousands of developers. If you want to talk with other developers, just scan the following QR Code in WeChat with secret code _python wechaty_, join our **Wechaty Python Developers' Home**.

![Wechaty Friday.BOT QR Code](https://wechaty.js.org/img/friday-qrcode.svg)

Scan now, because other Wechaty Python developers want to talk with you too! (secret code: _python wechaty_)

## The World's Shortest Python ChatBot: 9 lines of Code

```python
from wechaty import Wechaty

import asyncio
async def main():
    bot = Wechaty()
    bot.on('scan', lambda status, qrcode, data: print('Scan QR Code to login: {}\nhttps://wechaty.js.org/qrcode/{}'.format(status, qrcode)))
    bot.on('login', lambda user: print('User {} logged in'.format(user)))
    bot.on('message', lambda message: print('Message: {}'.format(message)))
    await bot.start()

asyncio.run(main())
```

## Python Wechaty Developing Plan

We already have Wechaty in TypeScript, It will be not too hard to translate the TypeScript(TS) to Python(PY) because [wechaty](https://github.com/wechaty/wechaty) has only 3,000 lines of the TS code, they are well designed and de-coupled by the [wechaty-puppet](https://github.com/wechaty/wechaty-puppet/) abstraction. So after we have translated those 3,000 lines of TypeScript code, we will almost be done.

As we have already a ecosystem of Wechaty in TypeScript, so we will not have to implement everything in Python, especially, in the Feb 2020, we have finished the [wechaty-grpc](https://github.com/wechaty/grpc) service abstracting module with the [wechaty-puppet-service](https://github.com/wechaty/wechaty-puppet-service) implmentation.

The following diagram shows out that we can reuse almost everything in TypeScript, and what we need to do is only the block located at the top right of the diagram: `Wechaty (Python)`.

```ascii
  +--------------------------+ +--------------------------+
  |                          | |                          |
  |   Wechaty (TypeScript)   | |    Wechaty (Python)      |
  |                          | |                          |
  +--------------------------+ +--------------------------+

  +-------------------------------------------------------+
  |                 Wechaty Puppet Service                |
  |                                                       |
  |                (wechaty-puppet-service)               |
  +-------------------------------------------------------+

+---------------------  wechaty-grpc  ----------------------+

  +-------------------------------------------------------+
  |                Wechaty Puppet Abstract                |
  |                                                       |
  |                   (wechaty-puppet)                    |
  +-------------------------------------------------------+

  +--------------------------+ +--------------------------+
  |      Pad Protocol        | |      Web Protocol        |
  |                          | |                          |
  | wechaty-puppet-padplus   | |(wechaty-puppet-puppeteer)|
  +--------------------------+ +--------------------------+
  +--------------------------+ +--------------------------+
  |    Windows Protocol      | |       Mac Protocol       |
  |                          | |                          |
  | (wechaty-puppet-windows) | | (wechaty-puppet-macpro)  |
  +--------------------------+ +--------------------------+
```

## Example: How to Translate TypeScript to Python

There's a 100 lines class named `Image` in charge of downloading the WeChat image to different sizes.

It is a great example for demonstrating how do we translate the TypeScript to Python in Wechaty Way:

### Image Class Source Code

- TypeScript: <https://github.com/wechaty/wechaty/blob/master/src/user/image.ts>
- Python: <https://github.com/wechaty/python-wechaty/blob/master/src/wechaty/user/image.py>

If you are interested in the translation and want to look at how it works, it will be a good start from reading and comparing those two `Image` class files in TypeScript and Python at the same time.

## To-do List

- TS: TypeScript
- SLOC: Source Lines Of Code

### Wechaty Internal Modules

1. [ ] Class Wechaty @wj-mCat
    - TS SLOC(1160): <https://github.com/wechaty/wechaty/blob/master/src/wechaty.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation
1. [ ] Class Contact
    - TS SLOC(804): <https://github.com/wechaty/wechaty/blob/master/src/user/contact.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation
1. [ ] Class ContactSelf
    - TS SLOC(199): <https://github.com/wechaty/wechaty/blob/master/src/user/contact-self.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation
1. [ ] Class Message
    - TS SLOC(1054): <https://github.com/wechaty/wechaty/blob/master/src/user/message.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation
1. [ ] Class Room
    - TS SLOC(1194): <https://github.com/wechaty/wechaty/blob/master/src/user/room.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation
1. [ ] Class Image @wj-mCat
    - TS SLOC(60): <https://github.com/wechaty/wechaty/blob/master/src/user/image.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation
1. [x] Class Accessory @huan
    - TS SLOC(179): <https://github.com/wechaty/wechaty/blob/master/src/accessory.ts>
    - [x] Code
    - [x] Unit Tests
    - [ ] Documentation
1. [ ] Class Config @wj-mCat
    - TS SLOC(187): <https://github.com/wechaty/wechaty/blob/master/src/config.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation
1. [ ] Class Favorite
    - TS SLOC(52): <https://github.com/wechaty/wechaty/blob/master/src/user/favorite.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation
1. [ ] Class Friendship
    - TS SLOC(417): <https://github.com/wechaty/wechaty/blob/master/src/user/friendship.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation
1. [ ] Class MiniProgram
    - TS SLOC(70): <https://github.com/wechaty/wechaty/blob/master/src/user/mini-program.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation
1. [ ] Class RoomInvitation
    - TS SLOC(317): <https://github.com/wechaty/wechaty/blob/master/src/user/room-invitation.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation
1. [ ] Class Tag
    - TS SLOC(190): <https://github.com/wechaty/wechaty/blob/master/src/user/tag.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation
1. [ ] Class UrlLink
    - TS SLOC(107): <https://github.com/wechaty/wechaty/blob/master/src/user/url-link.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation

### Wechaty External Modules

1. [ ] Class FileBox
    - TS SLOC(638): <https://github.com/huan/file-box/blob/master/src/file-box.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation
1. [ ] Class MemoryCard
    - TS SLOC(376): <https://github.com/huan/memory-card/blob/master/src/memory-card.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation
1. [ ] Class WechatyPuppet
    - TS SLOC(1115): <https://github.com/wechaty/wechaty-puppet/blob/master/src/puppet.ts>
    - [ ] Code
    - [ ] Unit Tests
    - [ ] Documentation
1. [ ] Class WechatyPuppetHostie
    - TS SLOC(909): <https://github.com/wechaty/wechaty-puppet-service/blob/master/src/client/puppet-service.ts>

## Usage

WIP...

## Requirements

1. Python 3.7+

## Install

```shell
pip3 install wechaty
```

## See Also

- [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)

### Static & Instance of Class

- [Static variables and methods in Python](https://radek.io/2011/07/21/static-variables-and-methods-in-python/)

### Typings

- [PEP 526 -- Syntax for Variable Annotations - Class and instance variable annotations](https://www.python.org/dev/peps/pep-0526/#class-and-instance-variable-annotations)
  - [Python Type Checking (Guide)](https://realpython.com/python-type-checking/) by [Geir Arne Hjelle](https://realpython.com/team/gahjelle/)

## History

### v0.6 (Jun 19, 2020)

Python Wechaty Scala Wechaty **BETA** Released!

Read more from our Multi-language Wechaty Beta Release event from our blog:

- [Multi Language Wechaty Beta Release Announcement!](https://wechaty.js.org/2020/06/19/multi-language-wechaty-beta-release/)

### v0.4 (Mar 15, 2020) master

Welcome [@huangaszaq](https://github.com/huangaszaq) for joining the project! [#42](https://github.com/wechaty/python-wechaty/pull/42)

1. Add a friendly exception message for PyPI users. [#24](https://github.com/wechaty/python-wechaty/issues/24)

### v0.1 (Mar 8, 2020)

Welcome [@wj-Mcat](https://github.com/wj-Mcat) for joining the project! [#4](https://github.com/wechaty/python-wechaty/pull/4)

1. Starting translate TypeScript of Wechaty to Python
1. DevOps Setup
    1. Type Checking: mypy & pytype
    1. Unit Testing: pytest
    1. Linting: pylint, pycodestyle, and flake8
    1. CI/CD: GitHub Actions
1. Publish to PyPI automatically after the tests passed.

### v0.0.1 (Aug 25, 2018)

Project created, publish a empty module `wechaty` on PyPI.

## Related Projects

- [Wechaty](https://github.com/wechaty/wechaty) - Conversatioanl AI Chatot SDK for Wechaty Individual Accounts (TypeScript)
- [Python Wechaty](https://github.com/wechaty/python-wechaty) - Python WeChaty Conversational AI Chatbot SDK for Wechat Individual Accounts (Python)
- [Go Wechaty](https://github.com/wechaty/go-wechaty) - Go WeChaty Conversational AI Chatbot SDK for Wechat Individual Accounts (Go)
- [Java Wechaty](https://github.com/wechaty/java-wechaty) - Java WeChaty Conversational AI Chatbot SDK for Wechat Individual Accounts (Java)
- [Scala Wechaty](https://github.com/wechaty/scala-wechaty) - Scala WeChaty Conversational AI Chatbot SDK for WechatyIndividual Accounts (Scala)

## Badge

[![Wechaty in Python](https://img.shields.io/badge/Wechaty-Python-blue)](https://github.com/wechaty/python-wechaty)

```md
[![Wechaty in Python](https://img.shields.io/badge/Wechaty-Python-blue)](https://github.com/wechaty/python-wechaty)
```

## Stargazers over time

[![Stargazers over time](https://starchart.cc/wechaty/python-wechaty.svg)](https://starchart.cc/wechaty/python-wechaty)

## Contributors

<a href="https://github.com/wechaty/python-wechaty/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=wechaty/python-wechaty" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

## Support

Thanks the following supported Software. 

[![test image size](https://resources.jetbrains.com/storage/products/company/brand/logos/jb_beam.svg?_gl=1*1lb7oaa*_ga*MjE5ODE2MzAwLjE2MzYxODMyNTE.*_ga_V0XZL7QHEB*MTY0MTI2NzU5OS41LjEuMTY0MTI2NzY3OC4w&_ga=2.157122558.411488113.1641267600-219816300.1636183251)](https://jb.gg/OpenSourceSupport)

## Committers

1. [@huangaszaq](https://github.com/huangaszaq) -  Chunhong HUANG (黄纯洪)

## Creators

- [@wj-Mcat](https://github.com/wj-Mcat) - Jingjing WU (吴京京)
- [@huan](https://github.com/huan) - ([李卓桓](http://linkedin.com/in/zixia)) zixia@zixia.net

## Copyright & License

- Code & Docs © 2018 Wechaty Contributors <https://github.com/wechaty>
- Code released under the Apache-2.0 License
- Docs released under Creative Commons
