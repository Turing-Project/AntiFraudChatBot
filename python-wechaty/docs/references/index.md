
python-wechaty的接口非常人性化和轻量级，通过不同模块不同接口来完成定制化的功能。在这个章节中将会为你详细介绍不同模块下的接口细节。

## 模块

python-wechaty中所有模块都可直接从top-level来导入，例如：

```python
from wechaty import Wechaty, Message
```

### Wechaty 类

- [Class Wechaty](./wechaty)

```python
from wechaty import Wechaty
```

当开发者想要编写聊天机器人时，可通过面向函数式编程和面向对象编程两种模式：

* 面向函数编程

```python
import os, asyncio

from wechaty import Message, Wechaty

async def on_message(msg: Message):
    if msg.text() == 'ding':
        await msg.say('dong')

async def main():
    bot = Wechaty()
    bot.on('message',   on_message)

    await bot.start()
    print('[Python Wechaty] Ding Dong Bot started.')

asyncio.run(main())
```

* 面向对象编程

```python
import asyncio

from wechaty import (
    Wechaty, Contact, Message
)

class MyBot(Wechaty):
    async def on_message(self, msg: Message):
        if msg.text() == 'ding':
            await msg.say('dong')

asyncio.run(MyBot().start())
```

以上两种方式中，各有优劣，可是我推荐使用面向对象编程，这个在封装性和代码提示的角度上都对开发者比较友好。

### 用户相关模块

当开发者想要搜索联系人，主动给某个联系人发送消息时，此时需要主动加载联系人对象，然后发送消息。模块类型有：

> 推荐：所有系统初始化相关的任务都需要在ready事件触发之后执行。

- [Class Message](./message)
- [Class Contact](./contact)
  - [Class ContactSelf](./contact-self)
- [Class Room](./room)
  - [Class RoomInvitation](./room-invitation)
- [Class Friendship](./friendship)

⚠️ 注意：在python-wechaty中加载以上模块的方式：

* 面向函数式编程

```python
# bot：机器人实例对象，函数内可访问的对象，推荐使用单例模式来构建
contacts: List[Contact] = bot.Contact.find_all()
```

* 面向对象编程

```python
async def on_ready(self, payload):
    # self: 机器人实例对象，而且还有良好的代码自动提示的功能
    contacts: List[Contact] = self.Contact.find_all()
```
