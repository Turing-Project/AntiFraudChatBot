"""
Python Wechaty - https://github.com/wechaty/python-wechaty

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright Wechaty

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

import dataclasses
import json
import re
from typing import (
    Optional,
    Union,
    List
)

from datetime import datetime
from wechaty_puppet import (
    FileBox,
    MessagePayload,
    MessageQueryFilter,
    MessageType,
    get_logger
)

from wechaty.exceptions import WechatyPayloadError, WechatyOperationError
from wechaty.user.contact_self import ContactSelf
from wechaty.utils import timestamp_to_date

from ..accessory import Accessory
from .mini_program import MiniProgram
# TODO -> remove Sayable interface temporary
# from ..types import Sayable

from .contact import Contact
from .url_link import UrlLink
from .image import Image
from .room import Room


log = get_logger('Message')

SUPPORTED_MESSAGE_FILE_TYPES: List[MessageType] = [
    MessageType.MESSAGE_TYPE_ATTACHMENT,
    MessageType.MESSAGE_TYPE_EMOTICON,
    MessageType.MESSAGE_TYPE_IMAGE,
    MessageType.MESSAGE_TYPE_VIDEO,
    MessageType.MESSAGE_TYPE_AUDIO
]


# pylint: disable=R0904,R0903
class Message(Accessory[MessagePayload]):
    """
    接受和发送的消息都封装成Message对象。

    All of wechaty messages will be encapsulated as a Message object.

    you can get all of message attribute through publish method.
    """

    Type = MessageType

    def __init__(self, message_id: str):
        """
        the initialization for Message object which only receive the
        message_id data to fetch payload.
        """
        super().__init__()

        self.message_id = message_id

    def message_type(self) -> MessageType:
        """
        get the message type
        Notes:
            for more details, please refer to : https://github.com/wechaty/grpc/blob/master/proto/wechaty/puppet/message.proto#L9
        """
        return self.payload.type

    def __str__(self) -> str:
        """
        format string for message, which keep consistant with wechaty/wechaty
        refer to : https://github.com/wechaty/wechaty/blob/master/src/user/message.ts#L195
        """
        if not self.is_ready():
            return f'Message <{self.message_id}> is not ready'

        message_list = [
            'Message',
            f'#{self.message_type().name.lower()}',
            # talker can't be None
            f'[🗣 {self.talker()}',
        ]
        if self.room():
            message_list.append(f'@👥 {self.room()}]')

        if self.message_type() == MessageType.MESSAGE_TYPE_TEXT:
            message_list.append(f'\t{self.text()[:70]}')

        return ''.join(message_list)

    async def say(self, msg: Union[str, Contact, FileBox, UrlLink, MiniProgram],
                  mention_ids: Optional[List[str]] = None) -> Optional[Message]:
        """
        send the message to the conversation envrioment which is source of this message.

        If this message is from room, so you can send message to this room.

        If this message is from contact, so you can send message to this contact, not to room.
        Args:
            msg: the message object which can be type of str/Contact/FileBox/UrlLink/MiniProgram
            mention_ids: you can send message with `@person`, the only things you should do is to
                set contact_id to mention_ids.
        Examples:
            >>> message.say('hello')
            >>> message.say(Contact('contact_id'))
            >>> message.say(FileBox('file_path'))
            >>> message.say(UrlLink('url'))
            >>> message.say(MiniProgram('app_id'))
        Returns:
            Optional[Message]: if the message is sent successfully, return the message object.
        """
        log.info('say() <%s>', msg)

        if not msg:
            log.error('can"t say nothing')
            return None

        room = self.room()
        if room is not None:
            conversation_id = room.room_id
        else:
            talker = self.talker()
            if talker is None:
                raise WechatyPayloadError('Message must be from room/contact')
            conversation_id = talker.contact_id

        # in order to resolve circular dependency problems which is not for
        # typing, we import some modules locally.
        # TODO -> this is not good solution, we will fix it later.

        from .url_link import UrlLink
        from .mini_program import MiniProgram

        if isinstance(msg, str):
            message_id = await self.puppet.message_send_text(
                conversation_id=conversation_id,
                message=msg,
                mention_ids=mention_ids)
        elif isinstance(msg, Contact):
            message_id = await self.puppet.message_send_contact(
                conversation_id=conversation_id,
                contact_id=msg.contact_id,
            )
        elif isinstance(msg, FileBox):
            message_id = await self.puppet.message_send_file(
                conversation_id=conversation_id, file=msg)
        elif isinstance(msg, UrlLink):
            message_id = await self.puppet.message_send_url(
                conversation_id=conversation_id, url=json.dumps(dataclasses.asdict(msg.payload)))
        elif isinstance(msg, MiniProgram):
            assert msg.payload is not None
            message_id = await self.puppet.message_send_mini_program(
                conversation_id=conversation_id,
                mini_program=msg.payload)
        else:
            raise WechatyPayloadError('message type should be str, '
                                      'Contact/FileBox/UrlLink/MiniProgram')

        message = self.load(message_id)
        await message.ready()
        return message

    @classmethod
    async def find(cls, talker_id: Optional[str] = None,
                   message_id: Optional[str] = None,
                   room_id: Optional[str] = None,
                   text: Optional[str] = None,
                   to_id: Optional[str] = None,
                   message_type: Optional[MessageType] = None
                   ) -> Optional[Message]:
        """find the message from the server.

        Args:
            talker_id (Optional[str], optional): the id of talker.
            message_id (Optional[str], optional): the id of message.
            room_id (Optional[str], optional): the id of room.
            text (Optional[str], optional): you can search message by sub-string of the text.
            to_id (Optional[str], optional): the id of receiver.
            message_type (Optional[MessageType], optional): the type of the message
        Examples:
            >>> message = Message.find(message_id='message_id')
        Returns:
            Optional[Message]: if find the messages, return the first of it.
                               if can't find message, return None
        """
        log.info('Message find all <%s, %s, %s, <%s, %s, %s>', talker_id,
                 message_id, room_id, text, to_id, message_type)

        messages = await cls.find_all(
            talker_id=talker_id,
            message_id=message_id,
            room_id=room_id,
            text=text,
            to_id=to_id,
            message_type=message_type
        )
        if messages is None or len(messages) < 1:
            return None

        if len(messages) > 1:
            log.warning(
                'Message findAll() got more than one(%d) result',
                len(messages))
        return messages[0]

    @classmethod
    async def find_all(cls, talker_id: Optional[str] = None,
                       message_id: Optional[str] = None,
                       room_id: Optional[str] = None,
                       text: Optional[str] = None,
                       to_id: Optional[str] = None,
                       message_type: Optional[MessageType] = None
                       ) -> List[Message]:
        """find the message from the server.

        Args:
            talker_id (Optional[str], optional): the id of talker.
            message_id (Optional[str], optional): the id of message.
            room_id (Optional[str], optional): the id of room.
            text (Optional[str], optional): you can search message by sub-string of the text.
            to_id (Optional[str], optional): the id of receiver.
            message_type (Optional[MessageType], optional): the type of the message
        Examples:
            >>> message = Message.find_all(message_id='message_id')
        Returns:
            List[Message]: return all of the searched messages
        """
        log.info('Message find all <%s, %s, %s, <%s, %s, %s>', talker_id,
                 message_id, room_id, text, to_id, message_type)

        query_filter = MessageQueryFilter(
            from_id=talker_id,
            id=message_id,
            room_id=room_id,
            text=text,
            to_id=to_id,
            type=message_type
        )
        message_ids = await cls.get_puppet().message_search(query_filter)
        messages = [cls.load(message_id) for message_id in message_ids]
        return messages

    def talker(self) -> Contact:
        """get the talker of the message
        Args:
            None
        Examples:
            >>> message.talker()
        Raises:
            WechatyPayloadError: can't find the talker information from the payload
        Returns:
            Contact: the talker contact object
        """
        talker_id = self.payload.from_id
        if talker_id is None:
            raise WechatyPayloadError('message must be from Contact')
        return self.wechaty.Contact.load(talker_id)

    def to(self) -> Optional[Contact]:
        """get the receiver, which is the Contact type, of the message
        Args:
            None
        Examples:
            >>> message.to()
        Returns:
            Optional[Contact]: if the message is private to contact, return the contact object
                else return None
        """
        to_id = self.payload.to_id
        if to_id is None:
            return None
        return self.wechaty.Contact.load(to_id)

    def room(self) -> Optional[Room]:
        """get the room from the messge
        Args:
            None
        Examples:
            >>> msg.room()
        Returns:
            Optional[Room]: if the message is from room, return the contact object.
                else return .
        """
        room_id = self.payload.room_id
        if room_id is None or room_id == '':
            return None
        return self.wechaty.Room.load(room_id)

    def chatter(self) -> Union[Room, Contact]:
        """return the chat container object of the message. 

        If the message is from room,return the Room object. else return Contact object
        Args:
            None
        Examples:
            >>> msg.chatter()
        Returns:
            Optional[Room, Contact]: return the room/contact object
        """
        room: Optional[Room] = self.room()
        if room:
            return room
        talker: Contact = self.talker()
        return talker

    def text(self) -> str:
        """
        get message text

        获取对话的消息文本.
        Args:
            None
        Examples:
            >>> msg.text()
        Returns:
            str: the message text
        """
        if self.payload.text:
            return self.payload.text
        return ''

    async def to_recalled(self) -> Message:
        """
        Get the recalled message

        Args:
            None
        Examples:
            >>> msg.to_recalled()
        Returns:
            Message: the recalled message
        """
        if self.message_type() != MessageType.MESSAGE_TYPE_RECALLED:
            raise WechatyOperationError(
                'Can not call toRecalled() on message which is not'
                ' recalled type.')

        origin_message_id = self.text()
        if origin_message_id is None:
            raise WechatyPayloadError('Can not find recalled message')

        log.info('get recall message <%s>', origin_message_id)
        try:
            message = self.wechaty.Message.load(origin_message_id)
            await message.ready()
            return message
        except Exception as exception:
            error_info = 'can"t load or ready message payload {}'.format(
                str(exception.args)
            )

            log.error(error_info)
            raise WechatyOperationError(error_info)

    async def recall(self) -> bool:
        """
        Recall a message.

        Args:
            None
        Example:
            >>> msg.recall()
        Returns:
            bool: True if recall success, else False
        """
        log.info('Message recall')
        success = await self.puppet.message_recall(self.message_id)
        return success

    @classmethod
    def load(cls, message_id: str) -> Message:
        """
        Create a Mobile Terminated Message
        """
        return cls(message_id)

    def type(self) -> MessageType:
        """
        Get the type from the message.

        Args:
            None
        Examples:
            >>> msg.type()
        Returns:
            MessageType: the message type
        """
        return self.payload.type

    def is_self(self) -> bool:
        """
        Check if a message is sent by self

        Args:
            None
        Examples:
            >>> msg.is_self()
        Returns:
            bool: True if message is sent by self, else False
        """
        login_user: ContactSelf = self.wechaty.user_self()
        talker = self.talker()
        if talker is None:
            return False
        return talker.contact_id == login_user.contact_id

    async def mention_list(self) -> List[Contact]:
        """
        Get message mentioned contactList.

        Args:
            None
        Examples:
            >>> msg.mention_list()
        Returns:
            List[Contact]: the contact list mentioned in the message
        """
        log.info('Message mention_list')
        room = self.room()
        if self.type() != MessageType.MESSAGE_TYPE_TEXT or room is None:
            return []

        # Use mention list if mention list is available
        # otherwise, process the message and get the mention list

        if self.payload is not None and self.payload.mention_ids is not None:
            async def id_to_contact(contact_id: str) -> Contact:
                contact = self.wechaty.Contact.load(contact_id)
                await contact.ready()
                return contact

            # TODO -> change to python async best practice
            contacts = [
                await id_to_contact(contact_id)
                for contact_id in self.payload.mention_ids]
            return contacts

        # TODO -> have to check that mention_id is not in room situation
        return []

    async def mention_text(self) -> str:
        """
        get mention text

        Examples:
            >>> msg.mention_text()
        Returns:
            str: the message text without mention
        """
        text = self.text()
        room = self.room()

        mention_list = await self.mention_list()

        if room is None or len(mention_list) <= 0:
            return text

        async def get_alias_or_name(member: Contact) -> str:
            if room is not None:
                alias = await room.alias(member)
                if alias:
                    return alias
            return member.name

        # TODO -> change to python async best practice
        # flake8: disable=F841
        mention_names = [
            await get_alias_or_name(member)
            for member in mention_list]

        while len(mention_names) > 0:
            escaped_cur = mention_names.pop()
            pattern = re.compile(f'@{escaped_cur}(\u2005|\u0020|$)')
            text = re.sub(pattern, '', text)

        return text

    async def mention_self(self) -> bool:
        """
        Check if a message is mention self.
        Examples:
            >>> msg.mention_self()
        Returns:
            bool: True if message is mention self, else False
        """
        user_self: ContactSelf = self.wechaty.user_self()

        # check and ready for message payload
        await self.ready()

        # check by mention_ids not mention_list
        if self.payload is None or self.payload.mention_ids is None:
            return False
        return user_self.contact_id in self.payload.mention_ids

    async def ready(self) -> None:
        """
        sync load message
        Examples:
            >>> msg.ready()
        """
        log.debug('Message ready <%s>', self)
        if self.is_ready():
            return

        self.payload = await self.puppet.message_payload(self.message_id)

        if self.payload.from_id.strip() != '':
            talker = self.wechaty.Contact.load(self.payload.from_id)
            await talker.ready()
        if self.payload.room_id.strip() != '':
            room = self.wechaty.Room.load(self.payload.room_id)
            await room.ready()
        if self.payload.to_id.strip() != '':
            to_contact = self.wechaty.Contact.load(self.payload.to_id)
            await to_contact.ready()

    async def forward(self, to: Union[Room, Contact]) -> None:
        """
        Forward a message to a room or a contact.
        Args:
            to: the room or contact to forward to
        Examples:
            >>> msg.forward(room)
            >>> msg.forward(contact)
        """
        log.info('forward() <%s>', to)
        if to is None:
            raise WechatyPayloadError('to param not found')
        try:
            if isinstance(to, Room):
                to_id = to.room_id
            elif isinstance(to, Contact):
                to_id = to.contact_id
            else:
                raise WechatyPayloadError(
                    'expected type is <Room, Contact>, but get <%s>'
                    % to.__class__)
            print(to_id)
            await self.puppet.message_forward(to_id, self.message_id)

        # pylint:disable=W0703
        except Exception as exception:
            message = 'Message forward error <%s>' % exception.args
            log.error(message)
            raise WechatyOperationError(message)

    def date(self) -> datetime:
        """
        Message sent date.

        Note:
            For difference between python2 and python3, please check the following link:
            
            - https://docs.python.org/2.7/library/datetime.html#datetime.datetime
            - https://docs.python.org/3.7library/datetime.html#datetime.datetime
            
            for datetime.fromtimestamp. It’s common forthis to be restricted to years from 1970through 2038.
            
            `2145888000` is `2038-01-01 00:00:00 UTC` forsecond
            
            `2145888000` is `1970-01-26 04:04:48 UTC` formillisecond
        
        Examples:
            >>> msg.date()
        Returns:
            datetime: message sent date
        """
        if self.payload.timestamp > 2145888000:
            time = datetime.fromtimestamp(self.payload.timestamp / 1000)
        else:
            time = datetime.fromtimestamp(self.payload.timestamp)
        return timestamp_to_date(self.payload.timestamp)

    def age(self) -> int:
        """
        Returns the message age in seconds.
        Returns:
            int: message age in seconds
        """
        return (datetime.now() - self.date()).seconds // 1000

    async def to_file_box(self) -> FileBox:
        """
        Extract the Media File from the Message, and put it into the FileBox.

        Notes:
            ```
            File MessageType is : {
                MESSAGE_TYPE_ATTACHMENT,
                MESSAGE_TYPE_EMOTICON,
                MESSAGE_TYPE_IMAGE,
                MESSAGE_TYPE_VIDEO
            }
            ```
        Examples:
            >>> msg.to_file_box()
        Returns:
            FileBox: file box
        """
        log.info('Message to FileBox')
        if self.type() not in SUPPORTED_MESSAGE_FILE_TYPES:
            raise WechatyOperationError(
                f'this type <{self.type().name}> message can"t be converted to '
                f'FileBox'
            )
        msg_type: MessageType = self.type()
        if msg_type == MessageType.MESSAGE_TYPE_IMAGE:
            file_box = await self.puppet.message_image(self.message_id)
        else:
            file_box = await self.puppet.message_file(self.message_id)
        
        return file_box

    def to_image(self) -> Image:
        """
        Extract the Image File from the Message, so that we can use
        different image sizes.
        Examples:
            >>> msg.to_image()
        Returns:
            Image: image
        """
        log.info('Message to Image() for message %s', self.message_id)
        if self.type() != MessageType.MESSAGE_TYPE_IMAGE:
            raise WechatyOperationError(
                'current message type: %s, not image type'
                % self.type()
            )
        return self.wechaty.Image.create(self.message_id)

    async def to_contact(self) -> Contact:
        """
        Get Share Card of the Message
        Extract the Contact Card from the Message, and encapsulate it into
         Contact class
        Examples:
            >>> msg.to_contact()
        Returns:
            Contact: contact
        """
        log.info('Message to Contact')
        if self.type() != MessageType.MESSAGE_TYPE_CONTACT:
            raise WechatyOperationError(
                'current message type: %s, not contact type'
                % self.type()
            )

        contact_id = await self.puppet.message_contact(self.message_id)

        contact = self.wechaty.Contact.load(contact_id)
        await contact.ready()
        return contact

    async def to_url_link(self) -> UrlLink:
        """
        get url_link from message
        Examples:
            >>> msg.to_url_link()
        Returns:
            UrlLink: url_link
        """
        log.info('Message to UrlLink')
        if self.type() != MessageType.MESSAGE_TYPE_URL:
            raise WechatyOperationError(
                'current message type: %s, not url type'
                % self.type()
            )
        payload = await self.puppet.message_url(self.message_id)
        if payload is None:
            raise WechatyPayloadError(
                'can not get url_link_payload by message: %s'
                % self.message_id)
        return self.wechaty.UrlLink(payload)

    async def to_mini_program(self) -> MiniProgram:
        """
        get message mini_program
        Examples:
            >>> msg.to_mini_program()
        Returns:
            MiniProgram: mini_program
        """
        log.info('Message to MiniProgram <%s>', self.message_id)

        if self.type() != MessageType.MESSAGE_TYPE_MINI_PROGRAM:
            raise WechatyOperationError('not a mini_program type message')

        payload = await self.puppet.message_mini_program(
            self.message_id)
        if payload is None:
            raise WechatyPayloadError(
                'no miniProgram payload for message %s'
                % self.message_id
            )
        return self.wechaty.MiniProgram(payload)
