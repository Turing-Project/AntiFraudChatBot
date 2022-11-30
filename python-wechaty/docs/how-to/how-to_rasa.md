---
title: "Rasa Rest Connector"
author: wj-mcat
categories: tutorial
tags:
  - python
  - plugin
  - rasa
---

## Rasa Plugin

用于将Rasa Server对接到Python Wechaty中，让你的Bot拥有智能对话管理的能力。

### 一、Quick Start

#### 1.1 Rasa Server

首先你需要启动Rasa Server，推荐的脚本如下所示：

> 假设rasa模型都已经训练好，能够正常运行，如果对rasa还不是很熟悉的同学，可以参考[rasa-getting-started](https://github.com/BOOOOTBAY/rasa-getting-started)

```shell
rasa run --credentials credentials.yml \
  --cors "*" --debug --endpoints endpoints.yml --enable-api
```

#### 1.2 Rasa Plugin

如果想要在python-wechaty中使用此插件，可参考以下代码：

```shell
pip install wechaty-plugin-contrib
```

```python
"""rasa plugin bot examples"""
from __future__ import annotations

import asyncio
from wechaty import Wechaty  # type: ignore

from wechaty_plugin_contrib import (
    RasaRestPlugin,
    RasaRestPluginOptions
)

async def run():
    """async run method"""
    options = RasaRestPluginOptions(
        endpoint='your-endpoint',
        conversation_ids=['room-id', 'contact-id']
    )
    rasa_plugin = RasaRestPlugin(options)
    
    bot = Wechaty().use(rasa_plugin)
    await bot.start()

asyncio.run(run())
```

