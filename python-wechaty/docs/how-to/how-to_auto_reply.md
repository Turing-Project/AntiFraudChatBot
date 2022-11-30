---
title: "自动回复"
---

## 自动回复

自动回复也是我们日常生活工作中的一些高频使用场景，而回复内容不仅限于文字，还可以是图片，文件，链接以及小程序等等。比如你给机器人发“网易”，它会给你发送一个网易云音乐的小程序；你给它发一个”身份证“，它会给你发送身份证的正反面照片；...... 等等。

以上应用场景很常见，而且还有更多的实际应用案例可根据自己的需求来调整。

示例代码如下所示：

```python
import asyncio
from wechaty import Wechaty, MiniProgram  # type: ignore
from wechaty_puppet import (    # type: ignore
    FileBox
)

from wechaty_plugin_contrib import (
    AutoReplyRule,
    AutoReplyPlugin,
    AutoReplyOptions,
)

from wechaty_plugin_contrib.matchers import ContactMatcher

async def run():
    """async run method"""
    img_url = 'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy' \
              '/it/u=1257042014,3164688936&fm=26&gp=0.jpg'
    plugin = AutoReplyPlugin(options=AutoReplyOptions(
        rules=[
            AutoReplyRule(keyword='ding', reply_content='dong'),
            AutoReplyRule(keyword='七龙珠', reply_content='七龙珠'),
            AutoReplyRule(
                keyword='七龙珠',
                reply_content=FileBox.from_url(img_url, name='python.png')
            ),
            AutoReplyRule(
                keyword='网易-李白',
                reply_content=MiniProgram.create_from_json({...})
            )
        ],
        matchers=[
            ContactMatcher('秋客'),
        ]
    ))
    bot = Wechaty().use(plugin)
    await bot.start()

asyncio.run(run())
```

代码非常简单（API设计的很人性化），相信大家一眼就能够看懂，在此我就不做过多解释。