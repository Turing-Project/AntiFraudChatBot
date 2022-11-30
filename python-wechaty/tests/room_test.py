from typing import Union
import pytest
from wechaty.wechaty import Wechaty  # noqa


@pytest.mark.asyncio
async def test_room_owner(test_bot: Wechaty) -> None:
    owner = await test_bot.Room("fake_room").owner()
    await owner.ready()
    assert owner.contact_id == "wechaty_user"


@pytest.mark.asyncio
async def test_room_topic(test_bot: Wechaty) -> None:
    topic = await test_bot.Room("fake_room").topic()
    assert topic == "fake_room"


@pytest.mark.parametrize(
    ("room_name", "res"), [("test", "test_room"), ("fake", "fake_room"), ("wechaty", None)]
)
@pytest.mark.asyncio
async def test_room_find(test_bot: Wechaty, room_name: str, res: Union[str, None]) -> None:
    room = await test_bot.Room.find(room_name)
    name = room.room_id if room else None
    assert name == res


@pytest.mark.parametrize(
    ("room_name", "res"), [("test", 1), ("fake", 1), ("room", 2), ("wechaty", 0)]
)
@pytest.mark.asyncio
async def test_room_findall(test_bot: Wechaty, room_name: str, res: int) -> None:
    room = await test_bot.Room.find_all(room_name)
    assert len(room) == res
