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

from typing import TYPE_CHECKING
from dataclasses import asdict

from wechaty import Accessory
from wechaty_puppet import MiniProgramPayload, get_logger
from wechaty.utils import default_str

if TYPE_CHECKING:
    from wechaty.user import Message


log = get_logger('MiniProgram')


class MiniProgram(Accessory[MiniProgramPayload]):
    """
    mini_program object which handle the url_link content
    """
    def __init__(self, payload: MiniProgramPayload):
        """
        initialization for mini_program
        :param payload:
        """
        super().__init__()

        log.info('MiniProgram created')
        self._payload: MiniProgramPayload = payload

    @classmethod
    async def create_from_message(cls, message: Message) -> MiniProgram:
        """
        static create MiniProgram method
        :return:
        """
        log.info(f'loading the mini-program from message <{message}>')

        mini_program_payload = await cls.get_puppet().message_mini_program(
            message_id=message.message_id)

        mini_program = MiniProgram(mini_program_payload)
        return mini_program

    @classmethod
    def create_from_json(cls, payload_data: dict) -> MiniProgram:
        """
        create the mini_program from json data
        """
        log.info(f'loading the mini-program from json data <{payload_data}>')

        payload = MiniProgramPayload(**payload_data)

        mini_program = cls(payload=payload)
        return mini_program

    def to_json(self) -> dict:
        """
        save the mini-program to dict data
        """
        log.info(f'save the mini-program to json data : <{self.payload}>')
        mini_program_data = asdict(self.payload)
        return mini_program_data

    @property
    def app_id(self) -> str:
        """
        get mini_program app_id
        :return:
        """
        return default_str(self._payload.appid)

    @property
    def title(self) -> str:
        """
        get mini_program title
        :return:
        """
        return default_str(self._payload.title)

    @property
    def icon_url(self) -> str:
        """
        get mini_program icon url
        """
        return default_str(self._payload.iconUrl)

    @property
    def page_path(self) -> str:
        """
        get mini_program page_path
        :return:
        """
        return default_str(self._payload.pagePath)

    @property
    def user_name(self) -> str:
        """
        get mini_program user_name
        :return:
        """
        return default_str(self._payload.username)

    @property
    def description(self) -> str:
        """
        get mini_program description
        :return:
        """
        return default_str(self._payload.description)

    @property
    def thumb_url(self) -> str:
        """
        get mini_program thumb_url
        :return:
        """
        return default_str(self._payload.thumbUrl)

    @property
    def thumb_key(self) -> str:
        """
        get mini_program thumb_key
        :return:
        """
        return default_str(self._payload.thumbKey)
