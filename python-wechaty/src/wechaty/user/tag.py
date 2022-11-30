"""
Tag for Contact Message
"""
from __future__ import annotations

from typing import (
    Dict,
    # Optional,
    Union,
    TYPE_CHECKING
)

from collections import defaultdict

from wechaty.exceptions import WechatyOperationError
from wechaty_puppet import get_logger
from ..accessory import (
    Accessory,
)

if TYPE_CHECKING:
    from .contact import Contact
    from .favorite import Favorite

log = get_logger('Tag')


class Tag(Accessory):
    """
    tag object which handle the url_link content
    """
    _pool: Dict[str, 'Tag'] = defaultdict()

    tag_id: str

    def __init__(self, tag_id: str) -> None:
        """
        initialization for tag base class
        :param tag_id:
        """
        super().__init__()
        log.info('create tag %s', tag_id)

        self.tag_id = tag_id

    @classmethod
    def load(cls, tag_id: str) -> Tag:
        """
        load tag instance
        """
        if tag_id in cls._pool:
            return cls._pool[tag_id]

        new_tag = cls(tag_id)
        cls._pool[tag_id] = new_tag
        return new_tag

    @classmethod
    def get(cls, tag_id: str) -> Tag:
        """
        get tag objecr
        """
        log.info('load tag object %s', tag_id)
        return cls.load(tag_id)

    async def delete(self, target: Union[Contact, Favorite]) -> None:
        """
        remove tag from contact or favorite
        :param target:
        :return:
        """
        log.info('delete tag %s', self.tag_id)

        if target is Contact:
            await self.puppet.tag_contact_delete(tag_id=self.tag_id)
        elif target is Favorite:
            # TODO -> tag_favorite_delete not implement
            pass
            # await self.puppet.tag_contact_delete()
        else:
            raise WechatyOperationError('target param is required to be Contact or Favorite object')

    async def add(self, to: Union[Contact, Favorite]) -> None:
        """
        add tag to contact or favorite
        :param to:
        :return:
        """
        log.info('add tag to %s', str(to))
        if isinstance(to, Contact):
            await self.puppet.tag_contact_add(
                tag_id=self.tag_id, contact_id=to.contact_id
            )
        elif isinstance(to, Favorite):
            # TODO -> tag_favorite_add not implement
            pass
            # self.puppet.tag_favorite_add(self.tag_id, to)

    def remove(self, source: Union[Contact, Favorite]) -> None:
        """
        Remove this tag from Contact/Favorite

        tips : This function is depending on the Puppet Implementation,
        see [puppet-compatible-table](https://github.com/wechaty/
        wechaty/wiki/Puppet#3-puppet-compatible-table)
        :param source:
        :return:
        """
        log.info('remove tag for %s with %s',
                 self.tag_id,
                 str(source))
        try:
            if isinstance(source, Contact):
                self.puppet.tag_contact_remove(
                    tag_id=self.tag_id, contact_id=source.contact_id)
            elif isinstance(source, Favorite):
                # TODO -> tag_favorite_remove not implement
                pass
        except Exception as e:
            log.info('remove exception %s', str(e.args))
            raise WechatyOperationError('remove error')
