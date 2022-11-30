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

from typing import Union, List
import json
from datetime import datetime

from wechaty.exceptions import WechatyOperationError
from wechaty_puppet import RoomInvitationPayload, get_logger
from .contact import Contact
from ..types import Acceptable
from ..accessory import Accessory

log = get_logger('RoomInvitation')


class RoomInvitation(Accessory, Acceptable):
    """
    Room Invitation
    """

    def __init__(self, room_invitation_id: str):
        """
        initialization
        """
        super(Accessory, self).__init__()

        self.invitation_id: str = room_invitation_id
        log.info('__init__ () <%s>', self)

    def __str__(self) -> str:
        # this function should not have to log info
        # log.info('__str__ ()')
        msg = self.invitation_id if self.invitation_id is not None \
            else 'loading'
        return 'RoomInvitation <%s>' % msg

    async def to_str(self) -> str:
        """
        get room invitation string format description with async way
        """
        log.info('to_str()')
        payload = await self.puppet.room_invitation_payload(
            room_invitation_id=self.invitation_id)

        return ''.join([
            'RoomInvitation#',
            self.invitation_id,
            '<',
            payload.topic,
            ',',
            payload.inviter_id,
            '>',
        ])

    @classmethod
    def load(cls, room_invitation_id: str) -> RoomInvitation:
        """
        load RoomInvitation object
        :param room_invitation_id:
        :return:
        """
        log.info('load () <%s>', room_invitation_id)

        invitation = RoomInvitation(room_invitation_id)
        return invitation

    async def accept(self) -> None:
        """
        accept the room invitation
        """
        log.info('accept() <%s>', self)
        await self.puppet.room_invitation_accept(
            room_invitation_id=self.invitation_id)
        inviter = await self.inviter()
        topic = await self.topic()
        try:
            await inviter.ready()
            log.info(
                'accept() with room(%s) & inviter(%s) ready())',
                topic,
                inviter
            )
        except Exception as exception:
            message = 'accept() with room(%s) & inviter(%s) error' % (topic, inviter)
            log.error(message)
            raise WechatyOperationError(message)

    async def inviter(self) -> Contact:
        """
        get the inviter of the invitation
        """
        log.info('inviter() <%s>', self)
        payload = await self.puppet.room_invitation_payload(
            room_invitation_id=self.invitation_id)
        contact = self.wechaty.Contact.load(payload.inviter_id)
        return contact

    async def topic(self) -> str:
        """
        get the topic of the intivation
        """
        log.info('topic() <%s>', self)
        payload = await self.puppet.room_invitation_payload(
            room_invitation_id=self.invitation_id)
        return payload.topic

    async def member_count(self) -> int:
        """
        get the number of the invitation members
        """
        log.info('member_count() <%s>', self)
        payload = await self.puppet.room_invitation_payload(
            room_invitation_id=self.invitation_id)
        return payload.member_count

    async def member_list(self) -> List[Contact]:
        """
        get the members of the room invitation
        """
        log.info('member_list() <%s>', self)
        payload = await self.puppet.room_invitation_payload(
            room_invitation_id=self.invitation_id
        )
        member_ids = payload.member_ids

        members: List[Contact] = [
            self.wechaty.Contact.load(member_id)
            for member_id in member_ids]

        # TODO -> need add __aiter__ to member class [not async iterable]
        for member in members:
            await member.ready()
        return members

    async def date(self) -> datetime:
        """
        get the date of the room invitation
        """
        log.info('date() <%s>', self)
        payload = await self.puppet.room_invitation_payload(
            room_invitation_id=self.invitation_id
        )
        return payload.date

    async def age(self) -> int:
        """
        get the age of the invitation timespan
        """
        log.info('age() <%s>', self)
        payload = await self.puppet.room_invitation_payload(
            room_invitation_id=self.invitation_id
        )
        seconds = (datetime.now() - payload.date).seconds
        return seconds // 1000

    @classmethod
    async def from_json(cls,
                        payload: Union[str, RoomInvitationPayload]
                        ) -> RoomInvitation:
        """
        Load the room invitation info from disk
        """
        if isinstance(payload, str):
            log.info('from_json() <%s>', payload)
        else:
            log.info('from_json() <%s>', json.dumps(payload))

        if isinstance(payload, str):
            params = json.loads(payload)
            invitation_payload = RoomInvitationPayload(*params)
        else:
            invitation_payload = payload

        # TODO -> don't understand what this line code can influence
        await cls.get_puppet().room_invitation_payload(
            room_invitation_id=invitation_payload.id)

        return cls.get_wechaty().RoomInvitation. \
            load(invitation_payload.id)

    async def to_json(self) -> str:
        """
        Get the room invitation info when listened on room-invite event
        """
        log.info('to_json() <%s>', self)
        payload = await self.puppet.room_invitation_payload(
            room_invitation_id=self.invitation_id
        )
        return json.dumps(payload)
