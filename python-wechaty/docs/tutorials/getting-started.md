## 快速开始

1、 安装

```shell
pip install --upgrade wechaty
```

2、 设置TOKEN

```shell
export token=your_token_at_here
# or
export WECHATY_PUPPET_SERVICE_TOKEN=your_token_at_here
```

或者通过代码来设置环境变量:

```python
import os
os.environ['token'] = 'your_token_at_here'
# or 
os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = 'your_token_at_here'
```

3、 聊天机器人

```python
import asyncio

from wechaty import Wechaty

class MyBot(Wechaty):
    async def on_message(self, msg: Message):
        from_contact = msg.talker()
        text = msg.text()
        room = msg.room()
        if text == 'ding':
            conversation: Union[
                Room, Contact] = from_contact if room is None else room
            await conversation.ready()
            await conversation.say('dong')
            file_box = FileBox.from_url(
                'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/'
                'u=1116676390,2305043183&fm=26&gp=0.jpg',
                name='ding-dong.jpg')
            await conversation.say(file_box)

asyncio.run(MyBot().start())
```

以上代码展示了基于python-wechaty如何开发聊天机器人的整体步骤：安装、设置TOKEN环境变量以及编写聊天机器人。示例机器人代码可查看：[ding-dong-bot-oop.py](https://github.com/wechaty/python-wechaty-getting-started/blob/master/examples/basic/ding-dong-bot-oop.py)

## 快速上手

- [使用padlocal协议](./use_padlocal_getting_started.md)
- [使用web协议](./use_web_getting_started.md)
- [使用Paimon协议](./use_paimon_getting_started.md)
