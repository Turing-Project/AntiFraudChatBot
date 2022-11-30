---
title: Wechaty
---

> `Wechaty`类用来实例化机器人对象，控制机器人的整体逻辑，如：启动、注册监听事件、登录、注销等功能。
------
> 一个机器人就是`Wechaty`实例，所有用户相关模块都应该通过实例来获取，这样能保证服务连接的一致性，此外所有的逻辑应该以插件和事件订阅的形式组织，保证不同业务之间的隔离性以及业务内的内聚性。

::: wechaty.Wechaty.__init__
### 示例代码
(世界上最短的Python ChatBot：9行代码)
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
### WechatyOptions

创建一个wechaty实例的可选参数

**Kind**: global typedef  
**Properties**

| Name | Type | Description |
| :--- | :--- | :--- |
| profile | `string` | Wechaty Name.            When you set this:            `new Wechaty({profile: 'wechatyName'})`            it will generate a file called `wechatyName.memory-card.json`.            This file stores the bot's login information.            If the file is valid, the bot can auto login so you don't need to scan the qrcode to login again.            Also, you can set the environment variable for `WECHATY_PROFILE` to set this value when you start.            eg:  `WECHATY_PROFILE="your-cute-bot-name" node bot.js`. This field is deprecated, please use `name` instead. [see more](https://github.com/wechaty/wechaty/issues/2049) |
| puppet | `PuppetModuleName` \| `Puppet` | Puppet name or instance |
| puppetOptions | `Partial.` | Puppet TOKEN |
| ioToken | `string` | Io TOKEN |

::: wechaty.Wechaty.instance

::: wechaty.Wechaty.use

::: wechaty.Wechaty.on
### WechatyEventName

Wechaty类的事件类型

**Kind**: global typedef  
**Properties**

| Name | Type | Description |
| :--- | :--- | :--- |
| error | `string` | When the bot get error, there will be a Wechaty error event fired. |
| login | `string` | After the bot login full successful, the event login will be emitted, with a Contact of current logined user. |
| logout | `string` | Logout will be emitted when bot detected log out, with a Contact of the current login user. |
| heartbeat | `string` | Get bot's heartbeat. |
| friendship | `string` | When someone sends you a friend request, there will be a Wechaty friendship event fired. |
| message | `string` | Emit when there's a new message. |
| ready | `string` | Emit when all data has load completed, in wechaty-puppet-padchat, it means it has sync Contact and Room completed |
| room-join | `string` | Emit when anyone join any room. |
| room-topic | `string` | Get topic event, emitted when someone change room topic. |
| room-leave | `string` | Emit when anyone leave the room. |
| room-invite | `string` | Emit when there is a room invitation, see more in  [RoomInvitation](room-invitation.md)                                    If someone leaves the room by themselves, wechat will not notice other people in the room, so the bot will never get the "leave" event. |
| scan | `string` | A scan event will be emitted when the bot needs to show you a QR Code for scanning. &lt;/br&gt;                                    It is recommend to install qrcode-terminal\(run `npm install qrcode-terminal`\) in order to show qrcode in the terminal. |

### WechatyEventFunction

Wechaty类的事件所绑定的相关函数

**Kind**: global typedef  
**Properties**

| Name | Type | Description |
| :--- | :--- | :--- |
| error | `function` | \(this: Wechaty, error: Error\) =&gt; void callback function |
| login | `function` | \(this: Wechaty, user: ContactSelf\)=&gt; void |
| logout | `function` | \(this: Wechaty, user: ContactSelf\) =&gt; void |
| scan | `function` | \(this: Wechaty, url: string, code: number\) =&gt; void |
| heartbeat | `function` | \(this: Wechaty, data: any\) =&gt; void |
| friendship | `function` | \(this: Wechaty, friendship: Friendship\) =&gt; void |
| message | `function` | \(this: Wechaty, message: Message\) =&gt; void |
| ready | `function` | \(this: Wechaty\) =&gt; void |
| room-join | `function` | \(this: Wechaty, room: Room, inviteeList: Contact\[\],  inviter: Contact\) =&gt; void |
| room-topic | `function` | \(this: Wechaty, room: Room, newTopic: string, oldTopic: string, changer: Contact\) =&gt; void |
| room-leave | `function` | \(this: Wechaty, room: Room, leaverList: Contact\[\]\) =&gt; void |
| room-invite | `function` | \(this: Wechaty, room: Room, leaverList: Contact\[\]\) =&gt; void                                          see more in  [RoomInvitation](room-invitation.md) |

::: wechaty.Wechaty.start
### 示例代码
```python
from wechaty import Wechaty
import asyncio

async def main():
    bot = Wechaty()
    await bot.start()

asyncio.run(main())
```

::: wechaty.Wechaty.restart

::: wechaty.Wechaty.stop

::: wechaty.Wechaty.user_self

::: wechaty.Wechaty.self