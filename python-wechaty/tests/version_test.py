"""
version unit test
"""
# import pytest   # type: ignore

from wechaty.version import VERSION


def test_version() -> None:
    """
    Unit Test for version file
    """

    assert VERSION == '0.0.0', 'version should be 0.0.0'
