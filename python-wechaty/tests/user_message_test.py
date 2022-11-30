import pytest
from wechaty.wechaty import Wechaty


@pytest.mark.asyncio
async def test_mention_text_without_mentions(test_bot: Wechaty) -> None:
    """Test extracting mention text from a message without mentions"""
    msg = await test_bot.Message.find(message_id="no_mention")
    await msg.ready()
    text = await msg.mention_text()
    assert text == 'foo bar asd'


@pytest.mark.asyncio
async def test_mention_text_without_mentions_in_room(test_bot: Wechaty) -> None:
    """Test extracting mention text from a message without mentions"""
    msg = await test_bot.Message.find(message_id="room_no_mention")
    await msg.ready()
    text = await msg.mention_text()
    assert text == 'beep'


@pytest.mark.asyncio
async def test_mention_text_with_mentions_in_room(test_bot: Wechaty) -> None:
    """Test extracting mention text from a message without mentions"""
    msg = await test_bot.Message.find(message_id="room_with_mentions")
    await msg.ready()
    text = await msg.mention_text()
    assert text == 'test message asd'


@pytest.mark.asyncio
async def test_mention_text_with_mentions_and_alias_in_room(test_bot: Wechaty) -> None:
    """Test extracting mention text from a message without mentions"""
    msg = await test_bot.Message.find(message_id="room_with_mentions_and_alias")
    await msg.ready()
    text = await msg.mention_text()
    assert text == '123123 kkasd'


@pytest.mark.asyncio
async def test_mention_text_with_mentions_and_mismatched_alias(test_bot: Wechaty) -> None:
    """Test extracting mention text from a message without mentions"""
    msg = await test_bot.Message.find(message_id="room_with_mentions_and_alias_mismatched")
    await msg.ready()
    text = await msg.mention_text()
    assert text == '123123@Fake User beep'


@pytest.mark.asyncio
async def test_mention_text_with_mentions_but_not_mention_data(test_bot: Wechaty) -> None:
    """Test extracting mention text from a message without mentions"""
    msg = await test_bot.Message.find(message_id="room_with_text_mentions")
    await msg.ready()
    text = await msg.mention_text()
    assert text == '@Wechaty User @Test User @Fake Alias beep!!'
