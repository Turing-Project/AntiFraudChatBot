---
title: Message
---

> 接受和发送的消息都封装成`Message`对象。

::: wechaty.user.message.Message.say
### 示例代码
```python
import asyncio
from wechaty import Wechaty, Message
from wechaty import Wechaty, Contact, FileBox, UrlLink
class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        text = msg.text()
        # 1. 发送文字到联系人
        if text == "叮":
            await msg.say('咚')
            return
        # 2. 发送媒体文件到联系人
        if text == "媒体":
            file_box1 = FileBox.from_url('https://wechaty.github.io/wechaty/images/bot-qr-code.png', "bot-qr-code.png")
            file_box2 = FileBox.from_file('text.txt', "text.txt")
            await msg.say(file_box1)
            await msg.say(file_box2)
            return
        # 3. 发送名片到联系人
        if text == "名片":
            contact_card = self.Contact.load('lijiarui')  # 把`lijiarui`更改为您在微信中的任意联系人的姓名
            await msg.say(contact_card)
            return
        # 4. 发送链接到联系人
        if text == "链接":
            url_link = UrlLink.create(
                description='WeChat Bot SDK for Individual Account, Powered by TypeScript, Docker, and Love',
                thumbnail_url='https://avatars0.githubusercontent.com/u/25162437?s=200&v=4',
                title='Welcome to Wechaty',
                url='https://github.com/wechaty/wechaty',
            )
            await msg.say(url_link)
            return
        # 5. 发送小程序 (暂时只有`wechaty-puppet-macpro`支持该服务)
        if text == "小程序":
            miniProgram = self.MiniProgram.create_from_json({
                "appid": 'gh_0aa444a25adc',
                "title": '我正在使用Authing认证身份，你也来试试吧',
                "pagePath": 'routes/explore.html',
                "description": '身份管家',
                "thumbUrl": '30590201000452305002010002041092541302033d0af802040b30feb602045df0c2c5042b777875706c6f61645f31373533353339353230344063686174726f6f6d3131355f313537363035393538390204010400030201000400',
                "thumbKey": '42f8609e62817ae45cf7d8fefb532e83',
            })
            await msg.say(miniProgram)
            return
asyncio.run(MyBot().start())
```

::: wechaty.user.message.Message.talker
### 示例代码
```python
import asyncio
from wechaty import Wechaty, Message
class MyBot(Wechaty):
    async def on_message(self, msg: Message) -> None:
        print(msg.talker())
asyncio.run(MyBot().start())
```

::: wechaty.user.message.Message.find

::: wechaty.user.message.Message.find_all

::: wechaty.user.message.Message.talker

::: wechaty.user.message.Message.to
### 示例代码
```python
import asyncio
from wechaty import Wechaty, Message, Contact
class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        talker: Contact = msg.talker()
        text: str = msg.text()
        to_contact = msg.to()
        if to_contact:
            name = to_contact.name
            print(f"接收者: {name} 联系人: {talker.name} 内容: {text}")
        else:
            print(f"联系人: {talker.name} 内容: {text}")
asyncio.run(MyBot().start())
```


::: wechaty.user.message.Message.room
### 示例代码
```python
    import asyncio
    from wechaty import Wechaty, Message, Contact
    class MyBot(Wechaty):
    
        async def on_message(self, msg: Message) -> None:
            talker: Contact = msg.talker()
            text: str = msg.text()
            room = msg.room()
            if room:
                room_name = await room.topic()
                print(f"群聊名: {room_name} 联系人(消息发送者): {talker.name} 内容: {text}")
            else:
                print(f"联系人: {talker.name} 内容: {text}")
    asyncio.run(MyBot().start())
```

::: wechaty.user.message.Message.chatter

::: wechaty.user.message.Message.text
### 示例代码
```python
import asyncio
from wechaty import Wechaty, Message, Contact
class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        talker: Contact = msg.talker()
        text: str = msg.text()
        room = msg.room()
        if room:
            room_name = await room.topic()
            print(f"群聊名: {room_name} 联系人(消息发送者): {talker.name} 内容: {text}")
        else:
            print(f"联系人: {talker.name} 内容: {text}")
asyncio.run(MyBot().start())
```

::: wechaty.user.message.Message.to_recalled
### 示例代码
```python
    import asyncio
    from wechaty import Wechaty, Message
    from wechaty_puppet import MessageType
    class MyBot(Wechaty):
    
        async def on_message(self, msg: Message) -> None:
            if msg.type() == MessageType.MESSAGE_TYPE_RECALLED:
                recalled_message = await msg.to_recalled()
                print(f"{recalled_message}被撤回")
    asyncio.run(MyBot().start())
```

::: wechaty.user.message.Message.recall

::: wechaty.user.message.Message.type
### 示例代码
> `MessageType`是枚举类型
`from wechaty_puppet import MessageType`

* MessageType.MESSAGE_TYPE_UNSPECIFIED
* MessageType.MESSAGE_TYPE_ATTACHMENT
* MessageType.MESSAGE_TYPE_AUDIO
* MessageType.MESSAGE_TYPE_CONTACT
* MessageType.MESSAGE_TYPE_EMOTICON
* MessageType.MESSAGE_TYPE_IMAGE
* MessageType.MESSAGE_TYPE_TEXT
* MessageType.MESSAGE_TYPE_VIDEO
* MessageType.MESSAGE_TYPE_CHAT_HISTORY
* MessageType.MESSAGE_TYPE_LOCATION
* MessageType.MESSAGE_TYPE_MINI_PROGRAM 
* MessageType.MESSAGE_TYPE_TRANSFER 
* MessageType.MESSAGE_TYPE_RED_ENVELOPE 
* MessageType.MESSAGE_TYPE_RECALLED 
* MessageType.MESSAGE_TYPE_URL 

```python
import asyncio
from wechaty import Wechaty, Message
from wechaty_puppet import MessageType
class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        if msg.type() == MessageType.MESSAGE_TYPE_TEXT:
            print(f"这是个文本消息")
asyncio.run(MyBot().start())
```


::: wechaty.user.message.Message.is_self
### 示例代码
```python
import asyncio
from wechaty import Wechaty, Message
from wechaty_puppet import MessageType
class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        if msg.is_self():
            print("这个是Bot自己发出的消息")
        else:
            print("这是由别人发出的消息")
asyncio.run(MyBot().start())
```


::: wechaty.user.message.Message.mention_list
### 示例代码
- 消息事件表如下

|  | Web\(网页版\) | Mac PC Client\(苹果电脑端\) | iOS Mobile\(IOS系统移动端\) | android Mobile\(安卓移动端\) |
| :--- | :---: | :---: | :---: | :---: |
| \[有人@我\]的提示 | ✘ | √ | √ | √ |
| 区分移动端复制粘贴的魔法代码 `0d8197 \u0x2005` | ✘ | √ | √ | ✘ |
| 通过编程区分魔法代码`0d8197 \u0x2005`| ✘ | ✘ | ✘ | ✘ |
| 区分两个拥有相同群聊昵称的人的\[有人@我\]的提示  | ✘ | ✘ | √ | √ |

>注: `\u0x2005` 为不可见字符, 提及\(@\)的消息的格式一般为 `@Gary\u0x2005`

```python
import asyncio
from wechaty import Wechaty,  Message
class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        contact_mention_list = await msg.mention_list()
        print(contact_mention_list)
asyncio.run(MyBot().start())
```


::: wechaty.user.message.Message.mention_text
### 示例代码
```python
import asyncio
from wechaty import Wechaty, Message
class MyBot(Wechaty):
    # 原消息为 `@Gary Helloworld`
    async def on_message(self, msg: Message) -> None:
        print(await msg.mention_text()) # 打印`Helloworld`
asyncio.run(MyBot().start())
```


::: wechaty.user.message.Message.ready


::: wechaty.user.message.Message.forward
### 示例代码
```python
import asyncio
from wechaty import Wechaty,  Message
class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        room = await self.Room.find("wechaty")
        if room:
            await msg.forward(room)
            print("成功转发消息到wechaty群聊")
asyncio.run(MyBot().start())
```

::: wechaty.user.message.Message.date
### 示例代码
>举个例子, 有条消息是`8:43:01`发送的, 而当我们在Wechaty中接收到它的时候时间已经为 `8:43:15`, 那么这时 `age()`返回的值为`8:43:15 - 8:43:01 = 14 (秒)`


::: wechaty.user.message.Message.age

::: wechaty.user.message.Message.to_file_box
### 示例代码
> 文件类型的消息包括:
* MESSAGE_TYPE_ATTACHMENT
* MESSAGE_TYPE_EMOTICON
* MESSAGE_TYPE_IMAGE
* MESSAGE_TYPE_VIDEO

- 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://githubcom/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

::: wechaty.user.message.Message.to_image
### 示例代码
> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

::: wechaty.user.message.Message.to_contact
### 示例代码
> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

::: wechaty.user.message.Message.to_url_link
### 示例代码
> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

::: wechaty.user.message.Message.to_mini_program
### 示例代码
> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)
