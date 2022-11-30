### 一、Finder

插件中的部分业务功能通常是只针对于指定群聊或联系人，于是如何检索到指定对象，就成为开发的第一个问题。在此，我给大家介绍Finder，一个用于检索群聊，联系人的功能模块。

#### 1.1 Contact Finder

有很多种方式筛选联系人，比如最常见的通过`contact_id`、`contact name/alias`、`callback_func`等方法。使用方法如下所示：

```python
from __future__ import annotations
from typing import List
import re

from wechaty import Wechaty
from wechaty.user.contact import Contact
from wechaty.user.room import Room
from wechaty_puppet.schemas.room import RoomQueryFilter
from wechaty_plugin_contrib import (
    RoomFinder,
    FinderOption,
    ContactFinder
)

async def find_wechaty_contacts(bot: Wechaty) -> List[Contact]:
    contacts: List[Contact] = await bot.Contact.find_all('Baby')
    return contacts

async def contact_finders(bot: Wechaty) -> List[Contact]:
    """Contact Finder Example Code"""
    options: List[FinderOption] = [
        # 通过contact-id来筛选指定联系人
        'contact-id',
        # 通过Pattern（正则化表达式）来筛选群聊
        re.Pattern(r'Baby-\d'),
        # 通过回调函数来检索房间
        find_wechaty_contacts 
    ]
    contact_finder = ContactFinder(options)
    contacts: List[Contact] = await contact_finder.match(bot)
    return contacts
```

#### 1.2 Room Finder

```python
from __future__ import annotations
from typing import List
import re

from wechaty import Wechaty
from wechaty.user.contact import Contact
from wechaty.user.room import Room
from wechaty_puppet.schemas.room import RoomQueryFilter
from wechaty_plugin_contrib import (
    RoomFinder,
    FinderOption,
    ContactFinder
)

async def find_wechaty_rooms(bot: Wechaty) -> List[Room]:
    return await bot.Room.find_all(RoomQueryFilter(topic='Wechaty Room 1'))

async def room_finders(bot: Wechaty) -> List[Room]:
    """Room Finder Example Code"""
    room_finder_options: List[FinderOption] = [
        # 通过room-id来筛选指定群聊
        'room-id',
        # 通过Pattern（正则化表达式）来筛选群聊
        re.Pattern(r'Wechaty(.*)')
    ]
    room_finder = RoomFinder(room_finder_options)
    rooms: List[Room] = await room_finder.match(bot)
    return rooms
```

### 二、Matcher

### 2.1 Contact Matcher

### 2.2 Room Matcher

### 2.3 Message Matcher