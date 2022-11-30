# 使用Padlocal协议启动微信机器人

底层的对接实现是基于TypeScript语言，故无法直接在python-wechaty中使用该服务。可是Wechaty社区能够直接将其转化成对应的服务让多语言调用，从而实现：底层复用的特性。

整体步骤分为三步：

* 申请一个TOKEN
* 使用Docker启动Padlocal网关服务
* 使用python-wechaty连接服务并启动启动微信机器人


## 一、申请一个TOKEN
- 可以通过手机号注册来获得一个7天免费的TOKEN:[申请地址](http://pad-local.com)
- [TOKEN 说明](https://wechaty.js.org/docs/puppet-services/)
- 那如何获取长期Token呢？详细请看：[Everything-about-Wechaty](https://github.com/juzibot/Welcome/wiki/Everything-about-Wech aty)


## 二、使用Docker启动Padlocal网关服务
- 这一步可以在本机运行也可以在服务器上运行。
- 如果在服务器端运行，则须注意服务器相应端口防火墙规则需要打开
- 如果是在本地测试运行，则需要在启动机器人时指定环境变量SERVICE_ENDPOINT

### 2.1 脚本

```shell
# 设置环境变量

export WECHATY_LOG="verbose"
export WECHATY_PUPPET="wechaty-puppet-padlocal"
export WECHATY_PUPPET_PADLOCAL_TOKEN="puppet_padlocal_XXXXXX"

export WECHATY_PUPPET_SERVER_PORT="9001"
# 可使用代码随机生成UUID：import uuid;print(uuid.uuid4());
export WECHATY_TOKEN="1fe5f846-3cfb-401d-b20c-XXXXX"

docker run -ti \
  --name wechaty_puppet_service_token_gateway \
  --rm \
  -e WECHATY_LOG \
  -e WECHATY_PUPPET \
  -e WECHATY_PUPPET_PADLOCAL_TOKEN \
  -e WECHATY_PUPPET_SERVER_PORT \
  -e WECHATY_TOKEN \
  -p "$WECHATY_PUPPET_SERVER_PORT:$WECHATY_PUPPET_SERVER_PORT" \
  wechaty/wechaty:0.65
```

> 在此我默认所有的人都对[Docker](https://www.docker.com)的基本使用已经有了一定的了解，否则可以花几分钟去看看其[文档](https://www.docker.com/get-started)熟悉一下。

### 2.2 参数说明

* **WECHATY_PUPPET**: **标识**使用的哪个协议，一般和`token`类型的一一对应。比如当使用`padlocal`协议的话，那这个就是`wechaty-puppet-padlocal`，如果使用`web`协议的话，那这个就是`wechaty-puppet-wechat`。
* **WECHATY_PUPPET_PADLOCAL_TOKEN**: 这个协议是用来连接Padlocal的服务，目前是付费的。也就是在第一步中申请的。
* **WECHATY_PUPPET_SERVER_PORT**: 网关服务的接口，提供给`python-wechaty`来连接调用，如果服务部署在云服务器上，则需要保证该端口的可访问性。
* **WECHATY_TOKEN**: 当开发者在自己机器上启动一个网关服务时，需要通过`TOEKN`来做身份验证，避免服务被他人窃取。

以上代码只需要修改三个参数：`WECHATY_PUPPET_PADLOCAL_TOKEN`, `WECHATY_PUPPET_SERVER_PORT`, `WECHATY_TOKEN` 即可成功启动Token网关服务。

那网关服务启动成功之后，只需要编写`python-wechaty`的代码来连接即可。



## 三、使用python-wechaty连接服

### 3.1 本地测试和远端部署

当启动网关服务时，`Padlocal`会根据`WECHATY_TOKEN`来在[Wechaty服务接口](https://api.chatie.io/v0/hosties/__TOKEN__)上注册部署机器的`IP`和`端口`，然后python-wechaty会根据`WECHATY_TOKEN`在[Wechaty服务接口](https://api.chatie.io/v0/hosties/__TOKEN__)上获取对应的IP和端口。

可是很多小伙伴在实际开发的过程中，通常会出现`endpoint is not invalid`等错误信息，那是因为开发者有可能在本地启动网关服务或者服务器端口没有开放。

网关服务的部署通常是分为本地测试和远端部署，前者通常只是为了初学测试，后者是为了生产部署。如果是在生产部署时，只需要设置环境变量:

```shell
export WECHATY_PUPPET_SERVICE_TOKEN=1fe5f846-3cfb-401d-b20c-XXXXX
# or
export TOKEN=1fe5f846-3cfb-401d-b20c-XXXXX
# or
export token=1fe5f846-3cfb-401d-b20c-XXXXX
```

可是如果是在本地测试时，则通过ENDPOINT来找到启动的网关服务。

```shell
export WECHATY_PUPPET_SERVICE_TOKEN=1fe5f846-3cfb-401d-b20c-XXXXX
# or
export TOKEN=1fe5f846-3cfb-401d-b20c-XXXXX
# or
export token=1fe5f846-3cfb-401d-b20c-XXXXX

export WECHATY_PUPPET_SERVICE_ENDPOINT=127.0.0.1:9001
# or
export ENDPOINT=127.0.0.1:9001
# or
export endpoint=127.0.0.1:9001
```

### 3.2 TOKEN的作用

总而言之:

* 如果是公网环境下，可只需要设置`TOKEN`即可（因为你的token已经注册在chatie server上，故可以获取到目标资源服务器的ip和port）
* 如果是内网环境下，可只需要使用`ENDPOINT`(`localhost:port`)来让python-wechaty连接目标资源服务器。

> 如果是token是padlocal类型，则在python-wechaty程序内部可直接设置`export endpoint=localhost:port`来连接Gateway Server。

当然，以上的写法是使用Bash的方式来设置环境变量，也是可以通过python代码来设置环境变量，详细可看：

```python
import os
os.environ['token'] = "1fe5f846-3cfb-401d-b20c-XXXXX"
os.environ['endpoint'] = "127.0.0.1:9001"
```

### 3.3 机器人启动代码

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
os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT'] = "127.0.0.1:9001"
asyncio.run(MyBot().start())
```
### 运行代码


欢迎各位品尝以上代码 🥳 

* **相关链接**
  * [python-wechaty](https://github.com/wechaty/python-wechaty)
  * [python-wechaty-getting-started](https://github.com/wechaty/python-wechaty-getting-started)