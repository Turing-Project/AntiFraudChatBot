"""
config unit test
"""
from typing import (
    Any,
    # Dict,
    Iterable,
)

import pytest

from wechaty_puppet import get_logger

# pylint: disable=C0103
log = get_logger('ConfigTest')

# pylint: disable=redefined-outer-name


# https://stackoverflow.com/a/57015304/1123955
@pytest.fixture(name='data', scope='module')
def fixture_data() -> Iterable[str]:
    """ doc """
    yield 'test'


def test_config(
        data: Any,
) -> None:
    """
    Unit Test for config function
    """
    print(data)

    assert data == 'test', 'data should equals test'


def test_get_logger() -> None:
    """test"""
    assert get_logger, 'log should exist'
