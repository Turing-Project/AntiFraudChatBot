"""unit test for urllink"""
from __future__ import annotations

from wechaty.user.url_link import UrlLink


def test_create():
    """unit test for creating"""
    UrlLink.create(
        url='https://github.com/wechaty/python-wechaty/issues/339',
        title='title',
        thumbnail_url='thu',
        description='simple desc'
    )
