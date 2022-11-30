---
title: Friendship
---

# class Friendship()
> 发送、接收好友请求和好友确认事件。
> [示例/Friend-Bot](https://github.com/wechaty/python-wechaty-getting-started/blob/master/examples/advanced/friendship-bot.py)


::: wechaty.user.friendship.Friendship.search

::: wechaty.user.friendship.Friendship.add
### 示例代码
```python
memberList = await room.memberList()
for member in memberList:
    await bot.Friendship.add(member, 'Nice to meet you! I am wechaty bot!')
```

::: wechaty.user.friendship.Friendship.contact
### 示例代码
```python
import asyncio
from wechaty import Wechaty, Friendship


class MyBot(Wechaty):

    async on_friendship(self, friendship: Friendship) -> None:
        contact = friendship.contact()
        await contact.ready()
        log_msg = f'receive "friendship" message from {contact.name}'
        print(log_msg)


asyncio.run(MyBot().start())
```

::: wechaty.user.friendship.Friendship.accept
### 示例代码
```python
import asyncio
from wechaty import Wechaty, Friendship

class MyBot(Wechaty):

    async on_friendship(self, friendship: Friendship) -> None:
        contact = friendship.contact()
        await contact.ready()

        if friendship.type() == FriendshipType.FRIENDSHIP_TYPE_RECEIVE:
            log_msg = 'accepted automatically'
            await friendship.accept()
            # if want to send msg, you need to delay sometimes

            print('waiting to send message ...')
            await asyncio.sleep(3)
            await contact.say('hello from wechaty ...')
            print('after accept ...')
        elif friendship.type() == FriendshipType.FRIENDSHIP_TYPE_CONFIRM:
            log_msg = 'friend ship confirmed with ' + contact.name

        print(log_msg)

asyncio.run(MyBot().start())
```

::: wechaty.user.friendship.Friendship.hello
### 示例代码
> 自动接受好友请求中包含消息为 `ding` 的好友请求

```python
import asyncio
from wechaty import Wechaty, Friendship


class MyBot(Wechaty):

    async on_friendship(self, friendship: Friendship) -> None:
        contact = friendship.contact()
        await contact.ready()

        if friendship.type() == FriendshipType.FRIENDSHIP_TYPE_RECEIVE and friendship.hello() == 'ding':
            log_msg = 'accepted automatically because verify messsage is "ding"'
            await friendship.accept()
            # if want to send msg, you need to delay sometimes

            print('waiting to send message ...')
            await asyncio.sleep(3)
            await contact.say('hello from wechaty ...')
            print('after accept ...')

asyncio.run(MyBot().start())
```

::: wechaty.user.friendship.Friendship.type

::: wechaty.user.friendship.Friendship.from_json