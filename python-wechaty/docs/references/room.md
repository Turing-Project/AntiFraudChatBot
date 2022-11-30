---
title: Room
---

微信群聊（组）的相关功能被封装在 `Room` 类中。

## Classes

[Room](room.md#Room)

微信群聊（组）的相关功能被封装在 `Room` 类中。

[示例/Room-Bot](https://github.com/wechaty/python-wechaty-getting-started/blob/master/examples/advanced/room_bot.py)

## Typedefs

[RoomQueryFilter](room.md#RoomQueryFilter)

过滤条件的类，包含两个 `str` 类型的字段 `topic`, `id` 对应群名称和群 id .[RoomEventName](room.md#RoomEventName)

群聊事件类型 [RoomEventFunction](room.md#RoomEventFunction)

群聊事件的方法 [RoomMemberQueryFilter](room.md#RoomMemberQueryFilter)

通过 `Room.member()` 可以搜索当前群里的某一个成员。

## Room

微信群聊（组）的相关功能被封装在 `Room` 类中。

[示例/Room-Bot](https://github.com/wechaty/python-wechaty-getting-started/blob/master/examples/advanced/room_bot.py)

**类型**: 全局类

**属性**

| 名称 | 类型 | 描述 |
| :--- | :--- | :--- |
| id | `str` | 获取群聊（组）对象的id. 此函数取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table) |

* [Room](room.md#Room)
  * _实例方法_
    * [.ready\(force_sync=False\)](room.md#Room+ready) ⇒ `None`
    * [.say\(textOrContactOrFileOrUrl, mention_ids\)](room.md#Room+say) ⇒ `Union[None, Message]`
    * [.on\(event, listener\)](room.md#Room+on) ⇒ `None`
    * [.add\(contact\)](room.md#Room+add) ⇒ `None`
    * [.delete\(contact\)](room.md#Room+delete) ⇒ `None`
    * [.quit\(\)](room.md#Room+quit) ⇒ `None`
    * [.topic\(\[newTopic\]\)](room.md#Room+topic) ⇒ `Optional[str]`
    * [.announce\(\[text\]\)](room.md#Room+announce) ⇒ `Optional[str]`
    * [.qr_code\(\)](room.md#Room+qr_code) ⇒ `str`
    * [.alias\(contact\)](room.md#Room+alias) ⇒ `Optional[str]`
    * [.has\(contact\)](room.md#Room+has) ⇒ `bool`
    * [.member_list\(\[query\]\)](room.md#Room+member_list) ⇒ `List[Contact]>`
    * [.member\(queryArg\)](room.md#Room+member) ⇒ `Optional[Contact]`
    * [.owner\(\)](room.md#Room+owner) ⇒ `Optional[Contact]`
    * [.avatar\(\)](room.md#room-owner-contact-or-null) ⇒ `FileBox`
  * _静态方法_
    * [.create\(contactList, \[topic\]\)](room.md#Room.create) ⇒ `Room`
    * [.find\(query\)](room.md#Room.find) ⇒ `Optional[Room]`
    * [.find_all\(\[query\]\)](room.md#Room.findAll) ⇒ `List[Room]`

### async def ready\(self, force_sync: `bool` = None\)  ⇒ `None`

同步 `Room` 的数据。

**类型**: [`Room`](room.md#Room)的实例方法 

**示例**

```python
await room.ready()
```

### async def say\(self, some_thing: `Union[str, Contact, FileBox, MiniProgram, UrlLink]`, mention_ids: `Optional[List[str]]` = None\)⇒ `Union[None, Message]`

向群（组）中发送消息，如果携带了联系人列表 `mention_list` 参数，将会在群里同时 @ 这些联系人。

> 注意: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**类型**: [`Room`](room.md#Room)的实例方法

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| textOrContactOrFileOrUrlLinkOrMiniProgram | `str` \| `Contact` \| `FileBox` \| `UrlLink` \| `MiniProgram` | 在房间内发送 `文本`, `媒体文件` 或者 `链接`. 您可以使用 [FileBox](https://github.com/wechaty/python-wechaty-puppet/tree/master/src/wechaty_puppet/file_box) 类来发送文件。  |
| ...mentionList | `List[contact_id]` | 在群聊内发送内容，如果提供了联系人的id列表, 将会一并提及\(@\)他\(她\)们|

#### 示例
```python
from wechaty import Wechaty, FileBox, UrlLink, MiniProgram
import asyncio


class MyBot(Wechaty):
    async def on_login(self, contact: Contact):
        # 等待登入
        room = await bot.Room.find('wechaty')  # 可以根据 room 的 topic 和 id 进行查找

        # 1. 向房间发送文本
        await room.say('Hello world!')

        # 2.发送语音文件到群聊
        file_box1 = FileBox.from_url(
            url='https://wechaty.github.io/wechaty/images/bot-qr-code.png', name='QRCode')
        file_box2 = FileBox.from_file("./test.txt")  # 注意路径，以及文件不能为空
        await room.say(file_box1)
        await room.say(file_box2)

        # 3. 发送名片到群聊
        contact_card = await self.Contact.find('master')
        await room.say(contact_card)

        # 4. 在群聊内发送文本, 并提及(@) `some_members_id`列表里面提供的人
        members = await special_room.member_list()  # 房间内的所有联系人对象
        some_members_id = [m.contact_id for m in members[:3]]
        await room.say('Hello world!', some_members_id)

        # 5. 在群聊内发送连接
        urlLink = UrlLink.create(
            description='WeChat Bot SDK for Individual Account, Powered by TypeScript, Docker, and Love',
            thumbnail_url='https://avatars0.githubusercontent.com/u/25162437?s=200&v=4',
            title='Welcome to Wechaty',
            url='https://github.com/wechaty/wechaty',
        )
        await room.say(urlLink)

        # 6. 发送小程序 (暂时只有`wechaty-puppet-macpro`支持该功能)
        miniProgram = self.MiniProgram.create_from_json({
            "appid": 'gh_0aa444a25adc',
            "title": '我正在使用Authing认证身份，你也来试试吧',
            "pagePath": 'routes/explore.html',
            "description": '身份管家',
            "thumbUrl": '30590201000452305002010002041092541302033d0af802040b30feb602045df0c2c5042b777875706c6f61645f31373533353339353230344063686174726f6f6d3131355f313537363035393538390204010400030201000400',
            "thumbKey": '42f8609e62817ae45cf7d8fefb532e83',
        })
        await room.say(mini_program)

asyncio.run(MyBot().start())
```

### def on\(self, event_name: `str`, func: `Callable`\) ⇒ `None`

**类型**: [`Room`](room.md#Room)的实例方法 


| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| event | [`RoomEventName`](room.md#RoomEventName) | 发出的微信事件 |
| listener | [`RoomEventFunction`](room.md#RoomEventFunction) | 收到事件所触发的函数 |

#### 示例 _\(Event:join \)_

```python
bot = Wechaty()
await bot.start()
# 等待机器人登入
room = await bot.Room.find("event-room") # 把`event-room`改为您在微信中加入的任意群聊的群聊名称

async def on_join(invitees, inviter):
    log.info('Bot' + 'EVENT: room-join - Room "%s" got new member "%s", invited by "%s"' %
                 (await room.topic(), ','.join(map(lambda c: c.name, invitees)), inviter.name))

if room:
    room.on('join', on_join)
```

#### 示例 _\(Event:leave \)_

```python
bot = Wechaty()
await bot.start()
# 等待机器人登入
room = await bot.Room.find("event-room") # 把`event-room`改为您在微信中加入的任意群聊的群聊名称

async def on_leave(leaver_list, remover):
    log.info('Bot' + '群聊事件: 离开 - "%s" leave(remover "%s"), bye bye' % (','.join(leaver_list), remover or 'unknown'))

if room:
    room.on('leave', on_leave)
```

#### 示例 _\(Event:topic \)_

```python
bot = Wechaty()
await bot.start()
# 等待机器人登入
room = await bot.Room.find("wechaty") # 把`wechaty`改为您在微信中加入的任意群聊的群聊名称

async def on_topic(topic, old_topic, changer):
    log.info('Bot' + 'Room EVENT: topic - changed from "%s" to "%s" by member "%s"' % (old_topic, topic, changer.name()))

if room:
    room.on('topic', on_topic)
```

#### 示例 _\(Event:invite \)_

```python
bot = Wechaty()
await bot.start()
# 等待机器人登入
room = await bot.Room.find("wechaty") # 把`wechaty`改为您在微信中加入的任意群聊的群聊名称

async def on_invite(room_invitation):
    room_invitation.accept()

if room:
    room.on('invite', on_invite)
```

### async def add\(self, contact: `Contact`\) ⇒ `None`

将一个联系人添加到群聊

> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)
>
> 请参阅[网页版微信封闭了群聊接口](https://github.com/wechaty/wechaty/issues/1441)

**类型**: [`Room`](room.md#Room)类的实例方法

| 参数 | 类型 |
| :--- | :--- |
| contact | `Contact` |

#### 示例

```python
bot = Wechaty()
await bot.start()
# after logged in...
contact = await bot.Contact.find('lijiarui') # 把'lijiarui'改为您通讯录中的任意联系人
room = await bot.Room.find('wechaty')  # 把`wechaty`改为您在微信中加入的任意群聊的群聊名称
if room:
    try:
        await room.add(contact)
    except Exception  as e:
        log.error(e)
```

### async def delete\(self, contact: `Contact`\) ⇒ `None`

从房间中删除联系人, 该功能仅当机器人是房间的所有者\(群主\)时才有效

> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)
>
> 请参阅[网页版微信封闭了群聊接口](https://github.com/wechaty/wechaty/issues/1441)

**类型**: [`Room`](room.md#Room)类的实例方法

| 参数 | 类型 |
| :--- | :--- |
| contact | `Contact` |

#### 示例

```python
bot = Wechaty()
await bot.start()
# after logged in...
room = await bot.Room.find('wechat')   # change 'wechat' to any room topic in your wechat
contact = await bot.Contact.find('lijiarui')   # change 'lijiarui' to any room member in the room you just set
if room:
    try:
        await room.delete(contact)
    except Exception as e:
        log.error(e)
```

### async def quit\(self\) ⇒ `None`

机器人自行离开该群聊

> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**类型**: [`Room`](room.md#Room)类的实例方法 

**示例**

```python
await room.quit()
```

### async def topic\(self, new_topic: `str` = None\) ⇒ `Optional[str]`

设置/获取 群聊的名称

**类型**: [`Room`](room.md#Room)类的实例方法 

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| \[newTopic\] | `str` | 如果设置了该参数, 则会修改群聊名 |

#### 示例 _\(当任意联系人在群聊内发送消息, 您都会得到该群聊的名称 \)_

```python
import asyncio
from wechaty import Wechaty, Room, Contact, Message


class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        room: "Room" = msg.room()
        topic = await room.topic()
        print(f'群聊名: {topic}')

asyncio.run(MyBot().start())
```

#### 示例 _\(每当机器人登陆账号时, 机器人都会改变群聊的名字. \)_

```python
import asyncio
from wechaty import Wechaty, Room, Contact, Message

class MyBot(Wechaty):

    async def on_login(self, contact: Contact) -> None:
        room = await bot.Room.find('your room')  # 替换为您所加入的任意群聊
        old_topic = await room.topic()
        new_topic = await room.topic('Wechaty!')
        print(f'群聊名从{old_topic}改为{new_topic}')

asyncio.run(MyBot().start())

```

### async def announce\(self, announce_text: `str` = None\) ⇒ `Optional[str]`

`设置/获取` 群聊的公告

> 注意: 这个功能只有机器人是群主时才可以使用
>
> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**类型**: [`Room`](room.md#Room)类的实例方法 

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| \[text\] | `str` | 如果设置了这个参数, 则会更改群聊的公告 |

#### 示例 _\(当群聊内的任意联系人发送消息时, 您都会在控制台收到群公告的内容\)_

```python
import asyncio
from wechaty import Wechaty, Room, Contact, Message

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        room: "Room" = msg.room()
        announce = await room.announce()
        print(f'群公告为: {announce}')

asyncio.run(MyBot().start())
```

#### 示例 _\(每当机器人登陆账号时, 都会改变群聊公告的内容\)_

```python
import asyncio
from wechaty import Wechaty, Room, Contact, Message

class MyBot(Wechaty):

    async def on_login(self, contact: Contact) -> None:
        room = await bot.Room.find('your room')  # 替换为您所加入的任意群聊
        old_announce = await room.announce()
        new_announce = await room.announce('改变为wechaty!')
        print(f'群聊的公告从{old_announce}改变为{new_announce}')

asyncio.run(MyBot().start())


```

### async def qr_code\(self\) ⇒ `str`

获取可以用于扫描加入房间的二维码。

> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**类型**: [`Room`](room.md#Room)类的实例方法 

### async def alias\(self, member: `Contact`\) ⇒ `Optional[str]`

返回群聊内联系人的别名\(备注\)

**类型**: [`Room`](room.md#Room)类的实例方法 

**返回值**: `Optional[str]` - - 如果用户在群聊内有备注则返回字符串类型的备注, 没有则返回None

| 参数 | 类型 |
| :--- | :--- |
| contact | `Contact` |

#### 示例

```python
room = await bot.Room.find('your room')  # 要发送消息的群聊名
contact = await bot.Contact.find('lijiarui')  # 找到目标联系人
alias = await room.alias(contact)  # 获取该联系人的备注(别名)
print(f'{contact.name()}的别名是{alias}')
```

### async def has\(self, contact: `Contact`\)⇒ `bool`

检查这个群聊内是否有`contact`, 返回一个布尔类型的值

**类型**: [`Room`](room.md#Room)类的实例方法 

**返回值**: `bool` - 返回 `True` 如果群聊内有该联系人, 没有则返回 `false`.

| 参数 | 类型 |
| :--- | :--- |
| contact | `Contact` |

#### 示例 _\(检查好'lijiarui'是否在群聊'wechaty'内\)_

```python
contact = await bot.Contact.find('lijiarui')
room = await bot.Room.find('wechaty')
if contact and room:
    if await room.has(contact):
        print(f'{contact.name()} 在群聊wechaty房间内!')
    else:
        print(f'{contact.name()} 不在群聊wechaty房间内!')
```

### async def member_list(self, query: `Union[str, RoomMemberQueryFilter]` = None) ⇒ `List[Contact]>`

获取一个列表, 里面包含了所有联系人对象

#### definition

* `name`                 由联系人自身设置的名字, 叫做`name`, 等同于`Contact.name()`
* `roomAlias`            由联系人自身在群聊内设置的群别名\(备注, 昵称\), 叫做群昵称`roomAlias`
* `contactAlias`         由机器人为联系人设置的备注\(别名\), 叫做联系人备注`alias`, 等同于 `Contact.alias()`

**类型**: [`Room`](room.md#Room)类的实例方法 

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| \[query\] | [`RoomMemberQueryFilter`](room.md#RoomMemberQueryFilter) \| `str` | 可选的参数, 当时用 memberAll\(name:str\)时, 返回所有匹配到的成员, 包含名字, 群昵称, 联系人备注 |

#### 示例

```python
member_list = await room.member_list()
print(f'room all member list: {member_list}')

member_contact_list = await room.member_list('abc')
print(f'contact list with all name, room alias, alias are abc: {member_contact_list}')
```

### async def member(self, query: `Union[str, RoomMemberQueryFilter]` = None) ⇒ `Optional[Contact]`

查找一个房间里的联系人，如果获取到的联系人多于一个，则返回第一个。

**类型**: [`Room`](room.md#Room)类的实例方法 

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| queryArg | [`RoomMemberQueryFilter`](room.md#RoomMemberQueryFilter) \| `str` | When use member\(name:string\), return all matched members, including name, roomAlias, contactAlias |

#### 示例 _\(通过名字寻找联系人\)_

```python
room = await bot.Room.find('wechaty')
if room:
    member = await room.member('lijiarui')
    if member:
        print(f'wechaty 群聊内找到了联系人: {member.name()}')
    else:
        print(f'wechaty群聊内找不到该联系人')
```

#### 示例 _\(通过MemberQueryFilter类来查找\)_

```python
import asyncio
from wechaty import Wechaty, Room, Message
from wechaty_puppet.schemas.room import RoomMemberQueryFilter

class MyBot(Wechaty):

    async def on_message(self, msg: Message) -> None:
        room: "Room" = msg.room()
        if room:
            member = await room.member(RoomMemberQueryFilter(name="lijiarui"))
            if member:
                print(f'wechaty room got the member: {member.name}')
            else:
                print(f'cannot get member in wechaty room!')


asyncio.run(MyBot().start())
```

### async def owner\(self\) ⇒ `Optional[Contact]`

获取该群聊的群主.

> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**类型**: [`Room`](room.md#Room)类的实例方法  

**示例**

```python
owner = await room.owner()
```

### async def avatar\(self\) ⇒ `FileBox`

获取群聊的头像.

> 提示: 此功能取决于Puppet的实现, 详见 [Puppet兼容表](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table)

**类型**: [`Room`](room.md#Room)类的实例方法  

**示例**

```python
owner = await room.avatar()
```

### `@classmethod` async def create\(cls, contacts: `List[Contact]`, topic: `str`\) ⇒ [`Room`](room.md#Room)

创建一个新的群聊

**类型**: [`Room`](room.md#Room)类的静态方法

| 参数 | 类型 |
| :--- | :--- |
| contactList | `List` |
| \[topic\] | `str` |

#### 示例 _\(用联系人'lijiarui' 和 'juxiaomi'创建一个群聊, 群聊的名称为'ding - created'\)_

```python
helper_contact_a = await bot.Contact.find('lijiarui')
helper_contact_b = await bot.Contact.find('juxiaomi')
contact_list = [helper_contact_a, helper_contact_b]
print('机器人创建所用的联系人列表为: %s', contact_list.join(','))
room = await Room.create(contact_list, 'ding')
print('Bot createDingRoom() new ding room created: %s', room)
await room.topic('ding - created')  # 设置群聊名称
await room.say('ding - 创建完成')
```

### `@classmethod` async def find_all(cls, query: `Optional[Union[str, RoomQueryFilter, Callable[[Contact], bool]]]` = None) ⇒ `List[Room]`

通过过滤器寻找群聊: {topic: str \| RegExp}, 通过一个列表返回所有匹配的群聊对象

**类型**: [`Room`](room.md#Room)类的静态方法

| 参数 | 类型 |
| :--- | :--- |
| \[query\] | [`RoomQueryFilter`](room.md#RoomQueryFilter) |

#### 示例

```python
room_list = await bot.Room.find_all()
room_list = await bot.Room.find_all('wechaty')
```

### `@classmethod` async def find(cls, query: `Optional[Union[str, RoomQueryFilter, Callable[[Contact], bool]]]` = None) ⇒ `Optional[Room]`

通过过滤器寻找群聊: {topic: str \| RegExp}, 如果获取到了多个群聊, 则返回第一个

**类型**: [`Room`](room.md#Room)类的静态方法

**返回值**: `Optional[Room]` - 如果可以找到该群聊, 则返回该群聊的对象, 如果不能则返回None

| 参数 | 类型 |
| :--- | :--- |
| query | [`RoomQueryFilter`](room.md#RoomQueryFilter) |

#### 示例

```python
room_list = await bot.Room.find()
room_list = await bot.Room.find('wechaty')
```

## RoomQueryFilter

查找群聊的过滤器: {topic: string \| RegExp}

**类型**: 全局类型定义 

**属性**

| 参数 | 类型 | 描述 |
| :--- | :--- | :--- |
| topic | `str` | 群聊的名称| 
| id | `str` | 群聊的id | 

## RoomEventName

群聊类的事件类型(Room Class Event Type)

**类型**: 全局类型定义 

**属性**

| 名称 | 类型 | 描述 |
| :--- | :--- | :--- |
| join | `str` | 当有人进入群聊时触发. |
| topic | `str` | 获取群名事件, 当有人改变群聊名称时候 |
| leave | `str` | 当有人退出群聊时触发. <br/>`注意: 如果有人自己退出群聊，微信不会提醒房间里的其他人，所以机器人在此情况不会收到“leave”事件`。 |

## RoomEventFunction

群聊事件函数, 供开发者重写

**类型**: 全局类型定义 

**属性**

| 名称 | 类型 | 参数 | 描述| 
| :--- | :--- | :--- |:--- |
| on_room_join | `function` | \(self: Wechaty, room_invitation: RoomInvitation\); None | 有人加入群聊时触发 |
| on_room_topic | `function` | \(self: Wechaty, room: Room, new_topic: str, old_topic: str, changer: Contact, date: datetime\); None | 有人改变群聊名称时触发 |
| on_room_leave | `function` | \(self: Wechaty, room: Room, leavers: List\[Contact\],remover: Contact, date: datetime\); None | 有人被移出群聊时触发 |
| on_room_invite | `function` | \(self, room_invitation: RoomInvitation\); None | 有人邀请Bot加入群聊时触发 |
## RoomMemberQueryFilter

寻找群成员的一种方法Room.member\(\)

**类型**: 全局类型定义 

**属性**

| 名称 | 类型 | 描述 |
| :--- | :--- | :--- |
| name | `string` | 由联系人自身设置的名字, 叫做`name`, 等同于`Contact.name()`. |
| roomAlias | `string` | 由联系人自身在群聊内设置的群别名\(备注, 昵称\), 叫做群昵称`roomAlias` |
| contactAlias | `string` | 由机器人为联系人设置的备注\(别名\), 叫做联系人备注`alias`, 等同于 `Contact.alias()`. 详见[issues#365](https://github.com/wechaty/wechaty/issues/365) |
      
