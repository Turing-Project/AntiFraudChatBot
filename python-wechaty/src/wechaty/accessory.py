"""
Python Wechaty - https://github.com/wechaty/python-wechaty

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2018-now @copyright Wechaty

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    # overload,
    # cast,
    Optional,
    TypeVar,
    Generic,
)

from wechaty_puppet import (
    get_logger,
    Puppet,
)

from wechaty.exceptions import WechatyAccessoryBindingError

# pylint:disable=R0401
if TYPE_CHECKING:
    from .wechaty import Wechaty

log = get_logger('Accessory')

PayloadType = TypeVar('PayloadType')


class Accessory(Generic[PayloadType]):
    """
    Translate the function from TypeScript to Python
    See: https://github.com/wechaty/wechaty/blob/master/src/accessory.ts
    """

    _puppet: Optional[Puppet] = None
    _wechaty: Optional[Wechaty] = None

    abstract: bool = True

    def __init__(self) -> None:
        if self.abstract:
            raise WechatyAccessoryBindingError(
                'Do not instantiate class {cls} directly, sse with bot.{cls} instead. '
                'See https://github.com/wechaty/wechaty/issues/1217'.format(
                    cls=type(self).__name__
                )
            )

        self._payload: Optional[PayloadType] = None

    @property
    def payload(self) -> PayloadType:
        """
        get the payload object as a property
        :return:
        """
        if self._payload is None:
            raise ValueError(
                f'should ready()<sync> the {type(self).__name__} payload before get it, '
                'please call the <ready()> method'
            )
        return self._payload

    @payload.setter
    def payload(self, value: PayloadType) -> None:
        """
        :param value:
        :return:
        """
        if self._payload:
            log.warning('<%s> set payload more than once', self)
        self._payload = value

    def is_ready(self) -> bool:
        """
        check if payload is ready
        :return:
        """
        return self._puppet is not None and self._payload is not None

    @classmethod
    def set_puppet(cls, new_puppet: Puppet) -> None:
        """doc"""
        if cls._puppet is not None:
            raise AttributeError('can not set _puppet twice')
        cls._puppet = new_puppet

    @classmethod
    def set_wechaty(cls, new_wechaty: Wechaty) -> None:
        """doc"""
        if cls._wechaty is not None:
            raise AttributeError('can not set _wechaty twice')
        cls._wechaty = new_wechaty

    @classmethod
    def get_puppet(cls) -> Puppet:
        """doc"""
        if cls._puppet is None:
            raise AttributeError('puppet not found')
        return cls._puppet

    @classmethod
    def get_wechaty(cls) -> Wechaty:
        """doc"""
        if cls._wechaty is None:
            raise AttributeError('wechaty not found')
        return cls._wechaty

    @property
    def puppet(self) -> Puppet:
        """doc"""
        if self._puppet is None:
            raise AttributeError('puppet not set')
        return self._puppet

    @property
    def wechaty(self) -> Wechaty:
        """
        instance property
        """
        if self._wechaty is None:
            raise AttributeError('wechaty not set')
        return self._wechaty
