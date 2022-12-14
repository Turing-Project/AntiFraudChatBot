from __future__ import annotations
from ..accessory import Accessory as Accessory
from ..config import AT_SEPARATOR as AT_SEPARATOR, PARALLEL_TASK_NUM as PARALLEL_TASK_NUM
from .contact import Contact as Contact
from .message import Message as Message
from .mini_program import MiniProgram as MiniProgram
from .url_link import UrlLink as UrlLink
from _typeshed import Incomplete
from typing import Any, Callable, List, Optional, Union, overload
from wechaty.exceptions import WechatyOperationError as WechatyOperationError, WechatyPayloadError as WechatyPayloadError
from wechaty.user.contact_self import ContactSelf as ContactSelf
from wechaty.utils.async_helper import gather_with_concurrency as gather_with_concurrency
from wechaty_puppet import FileBox, RoomMemberQueryFilter, RoomPayload, RoomQueryFilter

log: Incomplete

class Room(Accessory[RoomPayload]):
    room_id: Incomplete
    def __init__(self, room_id: str) -> None: ...
    def on(self, event_name: str, func: Callable[..., Any]) -> None: ...
    def emit(self, event_name: str, *args: Any, **kwargs: Any) -> None: ...
    @classmethod
    async def create(cls, contacts: List[Contact], topic: str) -> Room: ...
    @classmethod
    async def find_all(cls, query: Optional[Union[str, RoomQueryFilter, Callable[[Contact], bool]]] = ...) -> List[Room]: ...
    @classmethod
    async def find(cls, query: Union[str, RoomQueryFilter, Callable[[Room], bool]] = ...) -> Optional[Room]: ...
    @classmethod
    def load(cls, room_id: str) -> Room: ...
    payload: Incomplete
    async def ready(self, force_sync: bool = ..., load_members: bool = ...) -> None: ...
    @overload
    async def say(self, msg: str) -> Optional[Message]: ...
    @overload
    async def say(self, msg: str, mention_ids: List[str] = ...) -> Optional[Message]: ...
    @overload
    async def say(self, msg: Union[Contact, FileBox, UrlLink, MiniProgram]) -> Optional[Message]: ...

    async def add(self, contact: Contact) -> None: ...
    async def delete(self, contact: Contact) -> None: ...
    async def quit(self) -> None: ...
    async def topic(self, new_topic: str = ...) -> Optional[str]: ...
    async def announce(self, announce_text: str = ...) -> Optional[str]: ...
    async def qr_code(self) -> str: ...
    async def alias(self, member: Contact) -> Optional[str]: ...
    async def has(self, contact: Contact) -> bool: ...
    async def member_list(self, query: Union[str, RoomMemberQueryFilter] = ...) -> List[Contact]: ...
    async def member(self, query: Union[str, RoomMemberQueryFilter] = ...) -> Optional[Contact]: ...
    async def owner(self) -> Optional[Contact]: ...
    async def avatar(self) -> FileBox: ...
