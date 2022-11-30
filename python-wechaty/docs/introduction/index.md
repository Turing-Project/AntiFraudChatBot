---
title: "上手视频"
author: wj-mcat
categories: tutorial
tags:
  - news
  - python
image: /assets/2020/python-wechaty/live-coding.png
---

## Python-Wechaty

Wechaty 作为一个对话SDK，拥有适配多平台的优秀能力，同时还具备多语言的特性，今天我们将以一个简单的视频来介绍如何开始使用[Python-Wechaty](https://github.com/wechaty/python-wechaty)编写一个最简单的聊天机器人。

{% include iframe.html src="https://www.youtube.com/watch?v=KSELdGeJIzo" %}

## 上手步骤

### 1. 安装依赖包

```shell
pip install wechaty
```

### 2. 配置Token

Token的配置可以有多种方式：

方法一：通过环境变量来配置

```shell
export WECHATY_PUPPET_SERVICE_TOKEN='your-token'
```

方法二：通过python代码来配置

```python
import os
os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = 'your-token'
```

那如何获取长期Token呢？详细请看：[Everything-about-Wechaty](https://github.com/juzibot/Welcome/wiki/Everything-about-Wech aty)

### 3. 编写最简单的机器人代码

> talk is cheep, show you the code

```python
import asyncio
from wechaty import Wechaty, Message

class MyBot(Wechaty):
    async def on_message(self, msg: Message):
        talker = msg.talker()
        await talker.ready()
        if msg.text() == "ding":
            await talker.say('dong')
        elif msg.text() == 'image':
            file_box = FileBox.from_url(
                'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/'
                'u=1116676390,2305043183&fm=26&gp=0.jpg',
                name='ding-dong.jpg')
            await talker.say(file_box)

async def main():
    bot = MyBot()
    await bot.start()

asyncio.run(main())
```

以上代码即可完成一个最简单的`ding-dong`机器人，以及你给他发送一个`image`关键字，它能够给你回复一个图片，代码是不是非常简单呢？

这里还有功能更加强大的机器人[示例代码库](https://github.com/wechaty/python-wechaty-getting-started)，大家可以在这里来找与自己需求类似的机器人。

也欢迎大家持续关注[python-wechaty](https://github.com/wechaty/python-wechaty)，未来我们将持续发布一些短视频来介绍相关的用法。
