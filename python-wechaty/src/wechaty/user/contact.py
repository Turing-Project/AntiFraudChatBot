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

import types
import asyncio
import dataclasses
import json
from asyncio import Task
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
    Type,
    Union,
    Callable,
)

from pyee import AsyncIOEventEmitter
from wechaty_puppet import (
    ContactGender,
    ContactPayload,
    ContactQueryFilter,
    ContactType,
    get_logger,
    FileBox
)

# from wechaty.utils import type_check
from wechaty.exceptions import WechatyPayloadError, WechatyOperationError
from wechaty.config import PARALLEL_TASK_NUM
from wechaty.utils.async_helper import gather_with_concurrency

from ..accessory import Accessory

if TYPE_CHECKING:
    # pytype: disable=pyi-error
    from .tag import Tag
    # pytype: disable=pyi-error
    from .message import Message
    # pytype: disable=pyi-error
    from .url_link import UrlLink
    from .mini_program import MiniProgram
    

log = get_logger('Contact')


# pylint:disable=R0904
class Contact(Accessory[ContactPayload], AsyncIOEventEmitter):
    """
    contact object
    """
    _pool: Dict[str, 'Contact'] = {}

    def __init__(self, contact_id: str):
        """
        Init Contact object with id which will not be cached,

        so we suggest that you use load method to get a cached contact object

        Args:
            contact_id (str): the union identifier of contact

        Examples:
            >>> contact = bot.Contact(contact_id)
            >>> # but the following method is suggested
            >>> contact = bot.Contact.load(contact_id)
        """
        super().__init__()
        self.contact_id: str = contact_id
        self.payload: Optional[ContactPayload] = None

    def get_id(self) -> str:
        """
        Get the contact_id

        Examples:
            >>> contact_id = contact.get_id()

        Returns:
            str: the contact_id
        """
        return self.contact_id

    @classmethod
    def load(cls: Type[Contact], contact_id: str) -> Contact:
        """
        Load contact object, if it's not cached, create a new one and cache it.

        If you load it manually, you should call `ready()` to load the full info from puppet.

        Args:
            cls: the type of Contact
            contact_id: the union identifier of contact

        Examples:
            >>> contact = bot.Contact.load(contact_id)
            >>> await contact.ready()
            >>> is_friend = contact.is_friend()

        Returns:
            Contact: the contact object
        """
        # 1. check if it's cached
        if contact_id in cls._pool:
            return cls._pool[contact_id]

        # 2. create new contact object
        new_contact = cls(contact_id)
        cls._pool[contact_id] = new_contact
        return new_contact

    @classmethod
    def _filter_contacts(cls,
                         contacts: List[Contact],
                         query: Union[str, ContactQueryFilter, Callable[[Contact], bool]]) -> List[Contact]:

        func: Callable[[Contact], bool]
        if isinstance(query, str):

            def filter_func(contact: Contact) -> bool:
                payload = contact.payload
                if not payload:
                    return False
                if query in payload.alias or query in payload.name:
                    return True
                if query == payload.id or quit == payload.weixin:
                    return True
                return False
            func = filter_func

        elif isinstance(query, ContactQueryFilter):

            def filter_func(contact: Contact) -> bool:
                payload = contact.payload

                # to pass the type checking
                assert isinstance(query, ContactQueryFilter)
                if not payload:
                    return False

                if query.alias and query.alias in payload.alias:
                    return True
                if query.name and query.name in payload.name:
                    return True

                if query.id and query.id == payload.id:
                    return True
                if query.weixin and query.weixin == payload.weixin:
                    return True

                return False
            func = filter_func
        elif isinstance(types, types.FunctionType):
            func = query
        else:
            raise WechatyOperationError(f'Query Argument<{query}> is not correct')

        assert not not func
        contacts = list(filter(func, contacts))
        return contacts

    @classmethod
    async def find(cls,
                   query: Union[str, ContactQueryFilter, Callable[[Contact], bool]]
                   ) -> Optional[Contact]:
        """
        Find the first of contacts based on query, which can be string, ContactQueryFilter, or callable<filter> function.

        Args:
            query: the query body to build filter
            
        Examples:
            >>> # 1. find contacts based query string, will match one of: contact_id, weixin, name and alias
            >>> # what's more, contact_id and weixin will follow extract match, name and alias will follow fuzzy match
            >>> Contact.find('your-contact-id/weixin')   # find: <your-contact-id> == contact.contact_id
            >>> Contact.find('name/alias')     # find: <name> in contact.name

            >>> # 2. find contacts based ContactQueryFilter object, will match all fields
            >>> query = ContactQueryFilter(id='your-contact-id', weixin='weixin')     # find: <your-contact-id> == contact.contact_id
            >>> query = ContactQueryFilter(name='your-contact-name')      # find: <your-contact-name> in contact.name
            >>> Contact.find(query)

            >>> # 3. find contacts based on callable query function
            >>> def filter_contacts(contact: Contact) -> bool:
            >>>     if contact.contact_id == "your-contact-id":
            >>>         return True
            >>>     return False
            >>> Contact.find(filter_contacts)
        Returns:
            Contact: the contact object filtered by query or None
        """
        log.info('find() <%s, %s>', cls, query)

        contacts = await cls.find_all(query)
        if not contacts:
            return None
        return contacts[0]

    @classmethod
    async def find_all(cls: Type[Contact],
                       query: Optional[Union[str, ContactQueryFilter, Callable[[Contact], bool]]] = None
                       ) -> List[Contact]:
        """
        Find all contacts based on query, which can be string, ContactQueryFilter, or callable<filter> function.

        Args:
            query: the query body to build filter

        Examples:
            >>> # 1. find contacts based query string, will match one of: contact_id, weixin, name and alias
            >>> # what's more, contact_id and weixin will follow extract match, name and alias will follow fuzzy match
            >>> Contact.find_all('your-contact-id/weixin')   # find: <your-contact-id> == contact.contact_id
            >>> Contact.find_all('name/alias')     # find: <name> in contact.name

            >>> # 2. find contacts based ContactQueryFilter object, will match all fields
            >>> query = ContactQueryFilter(id='your-contact-id', weixin='weixin')     # find: <your-contact-id> == contact.contact_id
            >>> query = ContactQueryFilter(name='your-contact-name')      # find: <your-contact-name> in contact.name
            >>> Contact.find_all(query)

            >>> # 3. find contacts based on callable query function
            >>> def filter_contacts(contact: Contact) -> bool:
            >>>     if contact.contact_id == "your-contact-id":
            >>>         return True
            >>>     return False
            >>> Contact.find_all(filter_contacts)

        Returns:
            Contact: the contact object filtered by query
        """
        log.info('find_all() <%s, %s>', cls, query)

        # 1. load contacts with concurrent tasks
        contact_ids: List[str] = await cls.get_puppet().contact_list()

        contacts: List[Contact] = [cls.load(contact_id) for contact_id in contact_ids]
        tasks: List[Task] = [asyncio.create_task(contact.ready()) for contact in contacts]
        await gather_with_concurrency(PARALLEL_TASK_NUM, tasks)

        # 2. filter contacts
        if not query:
            return contacts

        contacts = cls._filter_contacts(contacts, query)
        return contacts

    async def ready(self, force_sync: bool = False) -> None:
        """
        Make contact ready for use which will load contact payload info.

        Args:
            force_sync: if true, it will re-fetch the data although it exist.

        Examples:
            >>> contact = Contact.load('contact-id')
            >>> await await contact.ready()

        Raises:
            WechatyPayloadError: when payload can"t be loaded
        """
        if force_sync or not self.is_ready():
            try:
                self.payload = await self.puppet.contact_payload(
                    self.contact_id)
                log.info('load contact <%s>', self)
            except IOError as e:
                log.info('can"t load contact %s payload, message : %s',
                         self.name,
                         str(e.args))

                raise WechatyPayloadError('can"t load contact payload')

    def __str__(self) -> str:
        """
        Get contact string representation.
        """
        if not self.is_ready() or not self.payload:
            return 'Contact <{}>'.format(self.contact_id)

        if self.payload.alias.strip() != '':
            identity = self.payload.alias
        elif self.payload.name.strip() != '':
            identity = self.payload.name
        elif self.contact_id.strip() != '':
            identity = self.contact_id
        else:
            identity = 'loading ...'
        return 'Contact <%s> <%s>' % (self.contact_id, identity)

    async def say(self, message: Union[str, Message, FileBox, Contact, UrlLink, MiniProgram]
                  ) -> Optional[Message]:
        """say something to contact, which can be text, image, file, contact, url

        Note:
            Its implementation depends on the puppet, so if you want to use this method, please check
            [Puppet](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table).

        Args:
            message: the message object to be sended to contact
        
        Examples:
            >>> contact = Contact.load('contact-id')
            >>> await contact.say('hello')
            >>> await contact.say(FileBox.from_file('/path/to/file'))
            >>> await contact.say(contact)
            >>> await contact.say(UrlLink('https://wechaty.js.org'))

            >>> # the data format of mini program should pre-stored
            >>> await contact.say(MiniProgram('username', 'appid'))

        Returns:
            Message: if the message is send successfully, return the message object, otherwise return None 
        """
        if not message:
            log.error('can"t say nothing')
            return None

        if not self.is_ready():
            await self.ready()

        # import some class because circular dependency
        from wechaty.user.url_link import UrlLink   # pylint: disable=import-outside-toplevel

        if isinstance(message, str):
            # say text
            msg_id = await self.puppet.message_send_text(
                conversation_id=self.contact_id,
                message=message
            )
        elif isinstance(message, Contact):
            msg_id = await self.puppet.message_send_contact(
                contact_id=message.contact_id,
                conversation_id=self.contact_id
            )

        elif isinstance(message, FileBox):
            msg_id = await self.puppet.message_send_file(
                conversation_id=self.contact_id,
                file=message
            )

        elif isinstance(message, UrlLink):
            # use this way to resolve circulation dependency import
            msg_id = await self.puppet.message_send_url(
                conversation_id=self.contact_id,
                url=json.dumps(dataclasses.asdict(message.payload), ensure_ascii=False)
            )
        elif isinstance(message, MiniProgram):
            msg_id = await self.puppet.message_send_mini_program(
                conversation_id=self.contact_id,
                mini_program=message.payload
            )

        else:
            log.info('unsupported tags %s', message)
            raise WechatyOperationError('unsupported tags')

        if msg_id is not None:
            msg = self.wechaty.Message.load(msg_id)
            await msg.ready()
            return msg

        return None

    @property
    def name(self) -> str:
        """get name of contact
        Examples:
            >>> contact = Contact.load('contact-id')
            >>> name: str = contact.name
        
        Returns:
            str: name of contact, if the payload is None, return empty string
        """
        if not self.payload:
            return ''
        return self.payload.name

    async def alias(self,
                    new_alias: Optional[str] = None
                    ) -> Union[None, str]:
        """
        Get or set alias of contact.
        
        If new_alias is given, it will set alias to new_alias,
        otherwise return current alias

        Notes:
            Setting aliases too often will result in failure (60 times per minute).

        Args:
            new_alias: the new alias of contact.

        Returns:
            alias: the current alias of contact
        """
        log.info('Contact alias <%s>', new_alias)
        if not self.is_ready():
            await self.ready()

        if self.payload is None:
            raise WechatyPayloadError('can"t load contact payload <%s>' % self)

        try:
            alias = await self.puppet.contact_alias(self.contact_id, new_alias)

            # reload the contact payload
            await self.ready(force_sync=True)
            return alias
        # pylint:disable=W0703
        except Exception as exception:
            log.info(
                'Contact alias(%s) rejected: %s',
                new_alias, str(exception.args))
        return None

    def is_friend(self) -> Optional[bool]:
        """
        Check if the contact is friend.

        Examples:
            >>> contact = Contact.load('contact-id')
            >>> is_friend = contact.is_friend()

        Returns:
            bool: if the contact is friend, return True, otherwise return False
        """
        if not self.payload:
            log.warning('please call `ready()` before `is_friend()`')
            return False

        if not hasattr(self.payload, 'friend'):
            log.warning('contact payload has no friend property, please post an issue to describe this problem, thanks!')
            return False
        return self.payload.friend

    def is_offical(self) -> bool:
        """
        Check if the contact is offical account.

        Notes:
            Its implementation depends on the puppet, so if you want to use this method, please check
            [Puppet](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table).

        Examples:
            >>> contact = Contact.load('contact-id')
            >>> is_offical = contact.is_offical()

        Returns:
            bool: if the contact is offical account, return True, otherwise return False
        """
        if self.payload is None:
            return False
        return self.payload.type == ContactType.CONTACT_TYPE_OFFICIAL

    def is_personal(self) -> bool:
        """
        Check if the contact is personal account.

        Notes:
            Its implementation depends on the puppet, so if you want to use this method, please check
            [Puppet](https://github.com/wechaty/wechaty/wiki/Puppet#3-puppet-compatible-table).

        Examples:
            >>> contact = Contact.load('contact-id')
            >>> is_personal = contact.is_personal()

        Returns:
            bool: if the contact is personal account, return True, otherwise return False
        """
        if self.payload is None:
            return False
        return self.payload.type == ContactType.CONTACT_TYPE_PERSONAL

    def type(self) -> ContactType:
        """
        Get type of contact, which can person, official, corporation, and unspecified.

        Examples:
            >>> contact = Contact.load('contact-id')
            >>> contact_type = contact.type()

        Returns:
            ContactType: the type of contact.
        """
        if self.payload is None:
            raise WechatyPayloadError('contact payload not found')
        return self.payload.type

    def star(self) -> Optional[bool]:
        """
        Check if the contact is a stared contact.

        Examples:
            >>> contact = Contact.load('contact-id')
            >>> is_star = contact.star()

        Returns:
            bool: if the contact is a stared contact, return True, otherwise return False.
        """
        if self.payload is None:
            return None
        return self.payload.star

    def gender(self) -> ContactGender:
        """
        Return the gender of contact.
        
        Returns:
            ContactGender: the object of contact gender
        """
        if self.payload is not None:
            return self.payload.gender
        return ContactGender.CONTACT_GENDER_UNSPECIFIED

    def province(self) -> Optional[str]:
        """
        Get the province of contact.

        Examples:
            >>> province: str = contact.province()

        Returns:
            Optional[str]: the province info in contact public info
        """
        if self.payload is None:
            return None
        return self.payload.province

    def city(self) -> Optional[str]:
        """
        Get the city of contact.

        Examples:
            >>> contact = Contact.load('contact-id')
            >>> city: str = contact.city()

        Returns:
            Optional[str]: the city info in contact public info
        """
        if self.payload is None:
            return None
        return self.payload.city

    async def avatar(self, file_box: Optional[FileBox] = None) -> FileBox:
        """
        Get or set the avatar of contact, which is a FileBox object

        Args:
            file_box: If given, it will set it as new avatar,
                else get the current avatar. Defaults to None.
        
        Examples:
            >>> contact = Contact.load('contact-id')
            >>> avatar = contact.avatar()

        Returns:
            FileBox: the avatar of contact
        """
        avatar = await self.puppet.contact_avatar(
            contact_id=self.contact_id, file_box=file_box)
        return avatar

    async def tags(self) -> List[Tag]:
        """
        Get the tags of contact which is a list of Tag object.

        Examples:
            >>> contact = Contact.load('contact-id')
            >>> tags = await contact.tags()

        Returns:
            List: the tags of contact
        """
        log.info('load contact tags for %s', self)
        tag_ids = await self.puppet.tag_contact_list(self.contact_id)
        tags = [self.wechaty.Tag.load(tag_id)
                for tag_id in tag_ids]
        return tags

    async def sync(self) -> None:
        """sync the contact info, this method will be deprecated in future,
            so we suggest use `ready()` instead
        """
        await self.ready()

    def is_self(self) -> bool:
        """
        Check if the contact is self.

        Examples:
            >>> contact = Contact.load('contact-id')
            >>> is_self = contact.is_self()

        Returns:
            bool: if the contact is self, return True, otherwise return False
        """
        login_user = self.wechaty.user_self()
        return login_user.contact_id == self.contact_id

    def weixin(self) -> Optional[str]:
        """
        Get the weixin union identifier of contact, which is specific for wechat account.

        Examples:
            >>> contact = Contact.load('contact-id')
            >>> weixin = contact.weixin()
            
        Returns:
            identifier: the weixin union identifier of contact
        """
        if self.payload is None:
            return None
        return self.payload.weixin
