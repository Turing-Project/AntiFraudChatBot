---
title: Contact
---

> 所有的微信联系人（朋友）都会被封装成一个`Contact`联系人对象。

::: wechaty.user.contact.Contact.__init__

::: wechaty.user.contact.Contact.get_id

::: wechaty.user.contact.Contact.load

::: wechaty.user.contact.Contact.find
### 示例代码
```python
import asyncio
from wechaty import Wechaty, Contact
from wechaty_puppet import ContactQueryFilter

class MyBot(Wechaty):

    async def on_login(self, contact: Contact) -> None:
        contact = await self.Contact.find(ContactQueryFilter(name="lijiarui"))
        contact = await self.Contact.find(ContactQueryFilter(alias="ruirui"))

asyncio.run(MyBot().start())
```

::: wechaty.user.contact.Contact.find_all
### 示例代码
```python
import asyncio
from wechaty import Wechaty, Contact
from wechaty_puppet import ContactQueryFilter

class MyBot(Wechaty):

    async def on_login(self, contact: Contact) -> None:
        contact = await self.Contact.find_all()  # 获取一个列表, 里面包含了Bot所有的联系人
        contact = await self.Contact.find_all(ContactQueryFilter(name="lijiarui"))  # 获取一个包含所有名字为lijiarui的联系人的列表
        contact = await self.Contact.find_all(ContactQueryFilter(alias="ruirui"))   # 获取一个包含所有别名(备注)为ruirui的联系人的列表

asyncio.run(MyBot().start())
```


::: wechaty.user.contact.Contact.ready


::: wechaty.user.contact.Contact.say
### 示例代码
```python
import asyncio
from wechaty import Wechaty, Contact, FileBox, UrlLink
from wechaty_puppet import ContactQueryFilter


class MyBot(Wechaty):

    async def on_login(self, contact: Contact) -> None:
        contact = await self.Contact.find(
            ContactQueryFilter(name="lijiarui"))  # 把`lijiarui`更改为您在微信中的任意联系人的姓名

        # 1. 发送文字到联系人
        await contact.say('welcome to wechaty!')

        # 2. 发送媒体文件到联系人
        fileBox1 = FileBox.from_url('https://wechaty.github.io/wechaty/images/bot-qr-code.png', "bot-qr-code.png")
        fileBox2 = FileBox.from_file('text.txt', "text.txt")
        await contact.say(fileBox1)
        await contact.say(fileBox2)

        # 3. 发送名片到联系人
        contactCard = self.Contact.load('lijiarui')  # 把`lijiarui`更改为您在微信中的任意联系人的姓名
        await contact.say(contactCard)

        # 4. 发送链接到联系人

        urlLink = UrlLink.create(
            description='WeChat Bot SDK for Individual Account, Powered by TypeScript, Docker, and Love',
            thumbnail_url='https://avatars0.githubusercontent.com/u/25162437?s=200&v=4',
            title='Welcome to Wechaty',
            url='https://github.com/wechaty/wechaty',
        )
        await contact.say(urlLink)

        # 5. 发送小程序 (暂时只有`wechaty-puppet-macpro`支持该服务)

        miniProgram = self.MiniProgram.create_from_json({
            "appid": 'gh_0aa444a25adc',
            "title": '我正在使用Authing认证身份，你也来试试吧',
            "pagePath": 'routes/explore.html',
            "description": '身份管家',
            "thumbUrl": '30590201000452305002010002041092541302033d0af802040b30feb602045df0c2c5042b777875706c6f61645f31373533353339353230344063686174726f6f6d3131355f313537363035393538390204010400030201000400',
            "thumbKey": '42f8609e62817ae45cf7d8fefb532e83',
        })

        await contact.say(miniProgram)

asyncio.run(MyBot().start())
```

::: wechaty.user.contact.Contact.name

::: wechaty.user.contact.Contact.alias
### 示例代码
```python
alias = await contact.alias()
if alias is None or alias == "":
    print('您还没有为联系人设置任何别名' + contact.name)
else:
    print('您已经为联系人设置了别名 ' + contact.name + ':' + alias)

```

::: wechaty.user.contact.Contact.is_friend

::: wechaty.user.contact.Contact.is_offical

::: wechaty.user.contact.Contact.is_personal

::: wechaty.user.contact.Contact.type
### 示例代码
> 注意: ContactType是个枚举类型.

```python
import asyncio
from wechaty import Wechaty, Message, ContactType

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        contact = msg.talker()
        print(contact.type() == ContactType.CONTACT_TYPE_OFFICIAL)

asyncio.run(MyBot().start())
```

::: wechaty.user.contact.Contact.star

::: wechaty.user.contact.Contact.gender
### 示例代码
> 注意: ContactGender是个枚举类型.

```python
import asyncio
from wechaty import Wechaty, Message, ContactGender


class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        contact = msg.talker()
        # 判断联系人是否为男性
        print(contact.gender() == ContactGender.CONTACT_GENDER_MALE)

asyncio.run(MyBot().start())
```


::: wechaty.user.contact.Contact.city

::: wechaty.user.contact.Contact.avatar
### 示例代码
```python
# 以类似 `1-name.jpg`的格式保存头像图片到本地
import asyncio
from wechaty import Wechaty, Message, FileBox

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        contact = msg.talker()
        avatar: "FileBox" = await contact.avatar()
        name = avatar.name
        await avatar.to_file(name, True)
        print(f"联系人: {contact.name} 和头像: {name}")

asyncio.run(MyBot().start())
```

::: wechaty.user.contact.Contact.tags

::: wechaty.user.contact.Contact.is_self

::: wechaty.user.contact.Contact.weixin

## Typedefs 类型定义

### [ContactQueryFilter](contact.md#ContactQueryFilter) 

用于搜索联系人对象的一个封装结构

| **属性名** | 类型     | **描述**                                                     |
| ---------- | -------- | ------------------------------------------------------------ |
| name       | `str` | 由用户本身(user-self)设置的名字, 叫做name                    |
| alias      | `str` | 由Bot为联系人设置的名字(备注/别名). 该值可以传入正则表达式用于搜索用户, 更多细节详见[issues#365](https://github.com/wechaty/wechaty/issues/365)和[源码](https://github.com/wechaty/python-wechaty-puppet/blob/master/src/wechaty_puppet/schemas/contact.py) |

