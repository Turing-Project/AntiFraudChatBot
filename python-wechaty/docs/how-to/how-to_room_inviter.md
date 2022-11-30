---
title: "自动回复&关键字入群插件"
---

经不可靠统计，大部分聊天机器人的初学者都是以：自动回复和关键字入群这两个基础功能上手，然后才会逐步开发更多更复杂的功能，在此我将介绍如何使用python-wechaty快速实现这两个功能。

> python-wechaty：一个面向所有IM平台的聊天机器人框架。

## 一、背景介绍

### 1.1 自动回复

有接触到微信公众号的同学都知道，它有一个自动回复的功能：你给它发送一个关键字，它就给你回复指定的内容，可以是纯文字，图片，视频等。

> 微信公众号的自动回复数量只有200个，虽然能够满足大部分的需求，可是如果扩充的话，便可以选择自定义开发。

而在微信中回复的内容又可以是什么呢？可以是：纯文字、带艾特消息@的文字、图片、动图（表情包）、视频，语音、视频、小程序以及好友名片等，这些消息内容在python-wechaty都能够使用简单的配置即可完成此功能。

### 1.2 关键字入群

目前有很多社区运营者都会面临着一些问题：

- 群人数一多，就只能够一个一个拉人入群。
- 有好几个用户/开发者群，某些群人数满了，无法动态拉到其他群。
- 一个人管理的活动太多，每次都需要根据用户的意图将其拉到指定的群，大大增加运营同学的工作量。
- 每天就光拉人入群就花了半天的时间，还有半天是在偷着休息，因为太累了。
- ......

以上问题都是我根据身边部分同学和朋友的吐槽中总结而来，为了帮助他们快速完成KPI，提升业绩，我做了以下AutoReplyPlugin和RoomInviterPlugin两个插件。

接下来我将介绍如何上手这两个插件，快速解决你们身边的一些问题。

## 二、安装 & 配置

编程环境要求python3.7+版本，以及一个token两个依赖包。

### 1.1 配置Token

什么是Token？为什么要配置Token？如何获取Token？

这么粗暴的灵魂三问在我们官网上早已有相关的[文档](https://github.com/juzibot/Welcome/wiki/Everything-about-Wechaty)，也欢迎各位去挖掘我们潜在的文档链接，说不定你就能找到属于你的One Piece，所以在此章节我就只介绍如何在python-wechaty中配置Token。

Token的配置可以有多种方式：

- 方法一：通过环境变量来配置

    ```bash
    export WECHATY_PUPPET_SERVICE_TOKEN='your-token'
    ```

- 方法二：通过python代码来配置

    ```python
    import os
    os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = 'your-token'
    ```

那如何获取长期Token呢？详细请看：[Everything-about-Wechaty](https://github.com/juzibot/Welcome/wiki/Everything-about-Wechaty)

### 1.2 安装依赖包

整个依赖包分为两个：`wechaty`以及`wechaty-plugin-contrib`，安装脚本如下所示：

```bash
# 安装python-wechaty包
pip install wechaty
# 安装插件库
pip install wechaty-plugin-contrib
```

前者为使用python-wechaty开发聊天机器人的基础依赖包，里面包含开发过程中的对象，甚至是自定义插件；后者为官方维护的插件库，在里面有很多常见的基础插件，让你快速解决日常学习工作中的自动化问题。同时也欢迎各位来提交PR，贡献属于自己的插件。

Wechaty社区欢迎各位优秀开发者共建Chatbot领域基础设施

## 三、关键字入群

关键字入群是很多社区运营同学的日常工作，也是最消耗体力的活儿，并没有很很复杂的脑力活儿。现在都0202年了，居然有同学还没有使用到自动化工具来提升工作效率，更有趣的事儿，他们大部分都有一个程序猿同事/同学/老公/老婆。为了让他们更好的帮助自己身边的人解决问题，关键字入群这个插件你们必须得安利一波儿～

### 3.1 功能介绍

当用户私聊你，发送一个关键字，然后聊天机器人会根据关键字寻找到对应的群，比如你给Wechaty官方机器人发送一个“wechaty”的关键字，它会将你拉到Wechaty的开发者群内，并发送欢迎语。

功能实际上很简单，如果从零开发的话，会让你无从下说。可是如果你使用python-wechaty的话，只需要几行简单的配置代码即可开发此功能。

`RoomInviterPlugin`  Is All You Need.

### 3.2 示例代码

最好的代码永远是最简单的代码

以下代码接近于人类语言，即使是新手，相信看完也知道如何开发专属聊天机器人：

```python
import asyncio
from typing import Dict
from wechaty import Wechaty
from wechaty_plugin_contrib.contrib import (
    RoomInviterOptions,
    RoomInviterPlugin
)
from wechaty_plugin_contrib.matchers import (
    MessageMatcher,
    RoomMatcher
)

async def run():
    """async run method"""
    rules: Dict[MessageMatcher, RoomMatcher] = {
        MessageMatcher('wechaty'): RoomMatcher('Wechaty开发者群（1）'),
        MessageMatcher('python-wechaty'): RoomMatcher('Python-Wechaty开发者群（2）'),
    }
    plugin = RoomInviterPlugin(options=RoomInviterOptions(
        name='python-wechaty关键字入群插件',
        rules=rules,
        welcome='欢迎入群 ～'
    ))
    bot = Wechaty().use(plugin)
    await bot.start()

asyncio.run(run())
```

在以上代码中，主要是分为三步：导入对象，注入规则，启动机器人。

- **导入对象**

    在`wechaty-plugin-contrib`的插件库中，所有的插件都会存在于`wechaty_plugin_contrib.contrib`下。大家一方面可以从源代码中查看的到最新的插件列表，也可以从README中查看到对应的插件列表。

    > 相信大家能够在这里找到灵感来源，或者一怒之下提交自己的定制插件。

- 注入**规则**

    在上述代码中，`rules`是一个规则字典，表示匹配到指定消息后就将消息发送者邀请到指定的群内；`plugin`就是封装核心逻辑组件，处理所有的自动化操作逻辑，开发者不需要关心这部分。

- 启动机器人

    启动机器人只需要调用一下start这个函数。

## 三、自动回复

自动回复也是我们日常生活工作中的一些高频使用场景，而回复内容不仅限于文字，还可以是图片，文件，链接以及小程序等等。比如你给机器人发“网易”，它会给你发送一个网易云音乐的小程序；你给它发一个”身份证“，它会给你发送身份证的正反面照片；...... 等等。

以上应用场景很常见，而且还有更多的实际应用案例可根据自己的需求来调整。

示例代码如下所示：

```python
import asyncio
from wechaty import Wechaty, MiniProgram  # type: ignore
from wechaty_puppet import (    # type: ignore
    FileBox
)

from wechaty_plugin_contrib import (
    AutoReplyRule,
    AutoReplyPlugin,
    AutoReplyOptions,
)

from wechaty_plugin_contrib.matchers import ContactMatcher

async def run():
    """async run method"""
    img_url = 'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy' \
              '/it/u=1257042014,3164688936&fm=26&gp=0.jpg'
    plugin = AutoReplyPlugin(options=AutoReplyOptions(
        rules=[
            AutoReplyRule(keyword='ding', reply_content='dong'),
            AutoReplyRule(keyword='七龙珠', reply_content='七龙珠'),
            AutoReplyRule(
                keyword='七龙珠',
                reply_content=FileBox.from_url(img_url, name='python.png')
            ),
            AutoReplyRule(
                keyword='网易-李白',
                reply_content=MiniProgram.create_from_json({...})
            )
        ],
        matchers=[
            ContactMatcher('秋客'),
        ]
    ))
    bot = Wechaty().use(plugin)
    await bot.start()

asyncio.run(run())
```

代码非常简单（API设计的很人性化），相信大家一眼就能够看懂，在此我就不做过多解释。

## 四、总结

python-wechaty有非常人性化的API，同时内置了很多高频功能插件库，提供给开发者能够快速上手开发出自己的小应用。

整个wechaty的目标是面向所有IM平台，打造一款通用聊天机器人框架，也欢迎各位关注并使用[python-wechaty](https://github.com/wechaty/python-wechaty)框架。
