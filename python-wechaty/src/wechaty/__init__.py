"""doc"""

#
# import types from wechaty_puppet
#

from wechaty_puppet import (
    FileBox,
    MessageType,
    MessagePayload,

    # Contact
    ContactGender,
    ContactType,
    ContactPayload,

    # Friendship
    FriendshipType,
    FriendshipPayload,

    # Room
    RoomPayload,
    RoomMemberPayload,

    # UrlLink

    # RoomInvitation
    RoomInvitationPayload,

    # Image
    ImageType,

    # Event
    EventType,
    EventReadyPayload,

    RoomQueryFilter,
    RoomMemberQueryFilter,
    FriendshipSearchQueryFilter,
    ContactQueryFilter,
    MessageQueryFilter,
    ScanStatus
)

from .config import (
    get_logger,
)
from .accessory import Accessory
from .plugin import (
    WechatyPlugin,
    WechatyPluginOptions
)
from .wechaty import (
    Wechaty,
    WechatyOptions,
)
from .user import (
    Contact,
    Favorite,
    Friendship,
    Image,
    Message,
    MiniProgram,
    Room,
    RoomInvitation,
    Tag,
    UrlLink,
)
from .exceptions import (
    WechatyError,
    WechatyConfigurationError,
    WechatyAccessoryBindingError,
    WechatyStatusError,
    WechatyPayloadError,
    WechatyOperationError,
    WechatyPluginError,
)

from .version import VERSION

__version__ = VERSION

__all__ = [
    'Accessory',
    'Contact',
    'Favorite',
    'FileBox',
    'Friendship',
    'get_logger',
    'Image',
    'Message',
    'MiniProgram',
    'Room',
    'RoomInvitation',
    'Tag',
    'UrlLink',
    'Wechaty',
    'WechatyOptions',

    'WechatyPlugin',
    'WechatyPluginOptions',

    'MessageType',
    'MessagePayload',

    # Contact
    'ContactGender',
    'ContactType',
    'ContactPayload',

    # Friendship
    'FriendshipType',
    'FriendshipPayload',

    # Room
    'RoomPayload',
    'RoomMemberPayload',

    # UrlLink

    # RoomInvitation
    'RoomInvitationPayload',

    # Image
    'ImageType',

    # Event
    'EventType',
    'EventReadyPayload',

    'ScanStatus',

    'RoomQueryFilter',
    'RoomMemberQueryFilter',
    'FriendshipSearchQueryFilter',
    'ContactQueryFilter',
    'MessageQueryFilter',

    # Error
    'WechatyError',
    'WechatyConfigurationError',
    'WechatyAccessoryBindingError',
    'WechatyStatusError',
    'WechatyPayloadError',
    'WechatyOperationError',
    'WechatyPluginError',
]
