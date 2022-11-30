"""doc"""
import asyncio
import logging
from typing import Optional, Union
from quart import Quart

from wechaty_puppet import FileBox, PuppetOptions

from wechaty import Wechaty, Contact, WechatyPlugin, WechatyOptions
from wechaty.user import Message, Room

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(filename)s <%(funcName)s> %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

log = logging.getLogger(__name__)


class SimpleServerWechatyPlugin(WechatyPlugin):
    """
    simple hello wechaty web server plugin
    """
    async def blueprint(self, app: Quart) -> None:
        @app.route('/wechaty')
        def hello_wechaty() -> str:
            """helo blueprint function"""
            return 'hello wechaty'


async def message(msg: Message) -> None:
    """back on message"""
    from_contact = msg.talker()
    text = msg.text()
    room = msg.room()
    if text == '#ding':
        conversation: Union[
            Room, Contact] = from_contact if room is None else room
        await conversation.ready()
        await conversation.say('dong')
        file_box = FileBox.from_url(
            'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/'
            'u=1116676390,2305043183&fm=26&gp=0.jpg',
            name='ding-dong.jpg')
        await conversation.say(file_box)

bot: Optional[Wechaty] = None


async def main() -> None:
    """doc"""
    # pylint: disable=W0603
    global bot
    options = WechatyOptions(
        host='127.0.0.1',
        port=5005,
        puppet_options=PuppetOptions(
            token='your-token'
        )
    )

    bot = Wechaty(
        options=options
    ).on('message', message)
    bot.use(SimpleServerWechatyPlugin())

    await bot.start()


asyncio.run(main())
