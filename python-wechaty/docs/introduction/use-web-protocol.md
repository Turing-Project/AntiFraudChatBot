# 使用免费Web协议

## 一、介绍

底层的对接实现是基于TypeScript语言，故无法直接在python-wechaty中使用该服务。可是Wechaty社区能够直接将其转化成对应的服务让多语言调用，从而实现：底层复用的特性。

整体步骤分为两步：

* 使用Docker启动web协议服务
* 使用python-wechaty连接服务

## 二、启动Web协议服务

```shell
docker pull wechaty/wechaty:0.65

export WECHATY_LOG="verbose"
export WECHATY_PUPPET="wechaty-puppet-wechat"
export WECHATY_PUPPET_SERVER_PORT="8080"
export WECHATY_TOKEN="python-wechaty-{uuid}"
export WECHATY_PUPPET_SERVICE_NO_TLS_INSECURE_SERVER="true"

# save login session
if [ ! -f "${WECHATY_TOKEN}.memory-card.json" ]; then
touch "${WECHATY_TOKEN}.memory-card.json"
fi

docker run -ti \
--name wechaty_puppet_service_token_gateway \
--rm \
-v "`pwd`/${WECHATY_TOKEN}.memory-card.json":"/wechaty/${WECHATY_TOKEN}.memory-card.json" \
-e WECHATY_LOG \
-e WECHATY_PUPPET \
-e WECHATY_PUPPET_SERVER_PORT \
-e WECHATY_PUPPET_SERVICE_NO_TLS_INSECURE_SERVER \
-e WECHATY_TOKEN \
-p "$WECHATY_PUPPET_SERVER_PORT:$WECHATY_PUPPET_SERVER_PORT" \
wechaty/wechaty:0.65
```

注意：

* WECHATY_TOKEN 必须使用生成的UUID来替换，不然直接使用该token来启动的服务很容易被他人盗窃。

小伙伴们可在python解释器中运行以下代码来获得随机TOKEN：
```python
# 例如：b2ff8fc5-c5a2-4384-b317-3695807e483f
import uuid;print(uuid.uuid4());
```

## 三、连接服务

当使用docker来启动web服务时，可分为在本地环境测试以及在远端环境中测试，在连接方式上有一些不一样。

### 3.1 本地WEB服务

当在计算机本地启动web服务后，可直接使用python-wechaty连接本地的服务，不通过token来获取对应的服务连接地址。示例代码如下：

```shell
export WECHATY_PUPPET_SERVICE_ENDPOINT=127.0.0.1:8080
```

或者

```python
import os
os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT'] = '127.0.0.1:8080'
```

> 当你的服务和python-wechaty机器人代码都部署在服务器中时，此时也属于本地服务，可使用此方法来配置。

### 3.2 远端服务

当把服务部署在远端服务器中时，要保证该计算机能够被外网访问到，且对应端口开放。例如在上述示例脚本中，比如保证服务器的`8080`端口开放，而你的服务器IP为：`10.12.123.23`，此时可直接设置服务连接地址：

```shell
export WECHATY_PUPPET_SERVICE_ENDPOINT=10.12.123.23:8080
```

或者

```python
import os
os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT'] = '10.12.123.23:8080'
```

## 四、编写代码

> talk is cheep, show you the code

```python
import asyncio
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

asyncio.run(MyBot().start())
```

欢迎各位品尝以上代码 🥳 
