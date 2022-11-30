# 使用Paimon协议

## 一、介绍

python原生支持paimon协议，不需要Token Gateway，简单方便。
[免费申请7天试用Token](https://wechaty.js.org/docs/puppet-services/paimon)


## 二、连接服务

### 2.1 本地测试和远端部署


```shell
export WECHATY_PUPPET_SERVICE_TOKEN=puppet_paimon_XXXXX
# or
export TOKEN=puppet_paimon_XXXXX
# or
export token=puppet_paimon_XXXXX
```



当然，以上的写法是使用Bash的方式来设置环境变量，也是可以通过python代码来设置环境变量，详细可看：

```python
import os
os.environ['token'] = "puppet_paimon_XXXXX"
```

## 三、示例代码

> talke is cheep, show you the code

```python
import asyncio, os
from typing import List, Optional, Union

from wechaty_puppet import FileBox  # type: ignore

from wechaty import Wechaty, Contact
from wechaty.user import Message, Room


class MyBot(Wechaty):

    async def on_message(self, msg: Message):
        """
        listen for message event
        """
        from_contact: Optional[Contact] = msg.talker()
        text = msg.text()
        room: Optional[Room] = msg.room()
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

os.environ['TOKEN'] = "1fe5f846-3cfb-401d-b20c-XXXXX"
asyncio.run(MyBot().start())
```

欢迎各位品尝以上代码 🥳 

* **相关链接**
  * [python-wechaty](https://github.com/wechaty/python-wechaty)
  * [python-wechaty-getting-started](https://github.com/wechaty/python-wechaty-getting-started)
