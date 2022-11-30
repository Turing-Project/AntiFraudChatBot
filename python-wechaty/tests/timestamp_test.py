"""
Unit test
"""
from wechaty.utils import timestamp_to_date


def test_timestamp_with_millisecond_precision() -> None:
    timestamp = timestamp_to_date(1600849574736)
    assert timestamp is not None


def test_timestamp_with_microsecond_precision() -> None:
    timestamp = timestamp_to_date(1600849792.367416)
    assert timestamp is not None
