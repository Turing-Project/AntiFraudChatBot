"""doc"""
from __future__ import annotations

from .contact         import Contact
from .favorite        import Favorite
from .friendship      import Friendship
from .image           import Image
from .message         import Message
from .mini_program    import MiniProgram
from .room            import Room
from .tag             import Tag
from .url_link        import UrlLink
from .room_invitation import RoomInvitation
from .contact_self import ContactSelf

# Huan(202003): is that necessary to put "name" to `__all__`?
# name = 'user'

__all__ = [
    'Contact',
    'Favorite',
    'Friendship',
    'Image',
    'Message',
    'MiniProgram',
    'Room',
    'Tag',
    'UrlLink',
    'RoomInvitation',
    'ContactSelf'
]
