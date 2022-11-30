"""
Python Wechaty - https://github.com/wechaty/python-wechaty
2020-now @ Copyright Wechaty

GitHub:
    TypeScript: https://github.com/wechaty/wechaty/blob/master/src/user/image.ts
    Python:     https://github.com/wechaty/python-wechaty/blob/master/src/wechaty/user/images.py

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

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
    Type,
)


from wechaty_puppet import (
    FileBox, ImageType, get_logger
)

from ..accessory import Accessory

log = get_logger('Image')


class Image(Accessory):
    """
    User Image class
    """

    def __str__(self) -> str:
        return 'Image<%s>' % self.image_id

    def __init__(
            self,
            image_id: str,
    ) -> None:
        """
        :param image_id:
        """
        super().__init__()
        log.info('init the message Image object <%s>', image_id)

        self.image_id = image_id

    @classmethod
    def create(cls: Type[Image], image_id: str) -> Image:
        """
        create image instance by image_id
        :param cls:
        :param image_id:
        :return:
        """
        log.info('@classmethod create(%s)', image_id)
        return cls(image_id)

    async def thumbnail(self) -> FileBox:
        """
        docstring
        :return:
        """
        log.info('thumbnail() for <%s>', self.image_id)
        image_file = await self.puppet.message_image(
            message_id=self.image_id, image_type=ImageType.IMAGE_TYPE_HD)
        return image_file

    async def hd(self) -> FileBox:
        """
        docstring
        :return:
        """
        log.info('hd() for <%s>', self.image_id)
        image_file = await self.puppet.message_image(
            message_id=self.image_id, image_type=ImageType.IMAGE_TYPE_HD)
        return image_file

    async def artwork(self) -> FileBox:
        """
        docstring
        :return:
        """
        log.info('artwork() for <%s>', self.image_id)
        image_file = await self.puppet.message_image(
            message_id=self.image_id, image_type=ImageType.IMAGE_TYPE_ARTWORK)
        return image_file
