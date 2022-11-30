"""
UrlLink for Contact Message
"""
from __future__ import annotations

from typing import (
    Optional,
    Type
)
from wechaty_puppet import UrlLinkPayload, get_logger

from wechaty.utils.link import get_url_metadata



log = get_logger('UrlLink')


class UrlLink:
    """
    url_link object which handle the url_link content
    """

    def __init__(
        self,
        payload: UrlLinkPayload,
    ):
        """
        initialization
        :param payload:
        """
        self.payload: UrlLinkPayload = payload

    @classmethod
    def create(
        cls: Type[UrlLink],
        url: str,
        title: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        description: Optional[str] = None
    ) -> UrlLink:
        """
        create urllink from url string
        """
        log.info('create url_link for %s', url)

        metadata = get_url_metadata(url)

        payload = UrlLinkPayload(url=url)
     
        payload.title = title or metadata.get('title', None)
        payload.thumbnailUrl = thumbnail_url or metadata.get('image', None)
        payload.description = description or metadata.get('description', None)
        return UrlLink(payload)

    def __str__(self) -> str:
        """
        UrlLink string format output
        :return:
        """
        return 'UrlLink<%s>' % self.payload.url

    @property
    def title(self) -> str:
        """
        get UrlLink title
        :return:
        """
        return self.payload.title or ''

    @property
    def thumbnailUrl(self) -> str:
        """
        get thumbnail url
        :return:
        """
        return self.payload.thumbnailUrl or ''

    @property
    def description(self) -> str:
        """
        get description
        :return:
        """
        return self.payload.description or ''

    @property
    def url(self) -> str:
        """
        get url
        :return:
        """
        return self.payload.url or ''
