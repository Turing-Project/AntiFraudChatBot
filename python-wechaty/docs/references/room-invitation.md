---
title: RoomInvitation
---

对群聊邀请事件的封装

## RoomInvitation

接受群聊的邀请

**类型**: 全局类

* [RoomInvitation](room-invitation.md#RoomInvitation)
  * [.accept\(\)](room-invitation.md#RoomInvitation+accept) ⇒ `None`
  * [.inviter\(\)](room-invitation.md#RoomInvitation+inviter) ⇒ `Contact`
  * [.topic\(\)](room-invitation.md#RoomInvitation+topic) ⇒ `str`
  * [~~.roomTopic\(\)~~](room-invitation.md#RoomInvitation+roomTopic) ⇒ `str`
  * [.date\(\)](room-invitation.md#RoomInvitation+date) ⇒ `datetime`
  * [.age\(\)](room-invitation.md#RoomInvitation+age) ⇒ `int`

### async def accept\(self\) ⇒ `None`

接受群聊邀请

**类型**: [`RoomInvitation`](room-invitation.md#RoomInvitation)的实例方法  

#### 示例

```python
import asyncio
from wechaty import Wechaty, RoomInvitation


class MyBot(Wechaty):

    async def on_room_invite(self, room_invitation: RoomInvitation) -> None:
        try:
            print("收到群聊邀请事件")
            await room_invitation.accept()
            print("已经自动接受")
        except Exception as e:
            print(e)

asyncio.run(MyBot().start())
```

### async def inviter\(self\) ⇒ `Contact`

获取群聊邀请的邀请人

**类型**: [`RoomInvitation`](room-invitation.md#RoomInvitation)的实例方法  

#### 示例

```python
import asyncio
from wechaty import Wechaty, RoomInvitation


class MyBot(Wechaty):

    async def on_room_invite(self, room_invitation: RoomInvitation) -> None:
        try:
            print("收到群聊邀请事件")
            inviter = await room_invitation.inviter()
            inviter_name = inviter.name
            print(f"收到来自{inviter_name}的群聊邀请")
        except Exception as e:
            print(e)

asyncio.run(MyBot().start())
```

### async def topic\(self\) ⇒ `str`

获取群聊邀请的群聊名

**类型**: [`RoomInvitation`](room-invitation.md#RoomInvitation)的实例方法  

#### 示例

```python
import asyncio
from wechaty import Wechaty, RoomInvitation


class MyBot(Wechaty):

    async def on_room_invite(self, room_invitation: RoomInvitation) -> None:
        try:
            room_name = await room_invitation.topic()
            print(f"收到来自{room_name}的群聊邀请")
        except Exception as e:
            print(e)

asyncio.run(MyBot().start())
```

### ~~async def roomTopic\(\)~~

**类型**: [`RoomInvitation`](room-invitation.md#RoomInvitation)的实例方法  
**已弃用:**: 请使用 topic\(\)

### async def date\(self\) ⇒ `datetime`

获取群聊邀请的日期

**类型**: [`RoomInvitation`](room-invitation.md#RoomInvitation)的实例方法  

### async def age\(self\) ⇒ `int`

获取当前距离已接收到的这条群聊邀请的时间的间隔, 单位为秒

举个例子, 有条群聊邀请是`8:43:01`发送的, 而当我们在Wechaty中接收到它的时候时间已经为 `8:43:15`, 那么这时 `age()`返回的值为 `8:43:15 - 8:43:01 = 14 (秒)`

**类型**: [`RoomInvitation`](room-invitation.md#RoomInvitation)的实例方法  
