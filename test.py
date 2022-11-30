"""
Python Wechaty - https://github.com/wechaty/python-wechaty
Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>
2020 @ Copyright Wechaty Contributors <https://github.com/wechaty>
Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.

You may obtain a copy of the License athttp://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""
import os
import asyncio
import subprocess

from urllib.parse import quote

from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)


async def on_message(msg: Message):
    """
    Message Handler for the Bot
    """
    if msg.text() == 'ding':
        await msg.say('dong')

        file_box = FileBox.from_url(
            'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/'
            'u=1116676390,2305043183&fm=26&gp=0.jpg',
            name='ding-dong.jpg'
        )
        try:
            await msg.say(file_box)
        except Exception as e:
            print("catch some errors:", e)


async def on_scan(
        qrcode: str,
        status: ScanStatus,
        _data,
):
    """
    Scan Handler for the Bot
    """
    print('Status: ' + str(status))
    print('View QR Code Online: https://wechaty.js.org/qrcode/' + quote(qrcode))


async def on_login(user: Contact):
    """
    Login Handler for the Bot
    """
    print(user)
    # TODO: To be written


async def main():
    """
    Async Main Entry
    """
    #
    # Make sure we have set WECHATY_PUPPET_SERVICE_TOKEN in the environment variables.
    # Learn more about services (and TOKEN) from https://wechaty.js.org/docs/puppet-services/
    #
    # It is highly recommanded to use token like [paimon] and [wxwork].
    # Those types of puppet_service are supported natively.
    # https://wechaty.js.org/docs/puppet-services/paimon
    # https://wechaty.js.org/docs/puppet-services/wxwork
    #
    # Replace your token here and umcommt that line, you can just run this python file successfully!
    # os.environ['token'] = 'puppet_paimon_your_token'
    # os.environ['token'] = 'puppet_wxwork_your_token'
    #
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    #for cloud-service
    os.environ['WECHATY_PUPPET_SERVICE_TOKEN']='puppet_padlocal_3f904c6aa9cd4c548944f6688a829707'
    os.environ['WECHATY_PUPPET']='wechaty-puppet-padlocal'
    os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT']='43.154.97.162:8788'

    # export WECHATY_PUPPET=wechaty-puppet-padlocal
    # export WECHATY_PUPPET_PADLOCAL_TOKEN=puppet_padlocal_3f904c6aa9cd4c548944f6688a829707
    # export WECHATY_PUPPET_SERVER_PORT=8788
    # export WECHATY_LOG=verbose

    #for local-service
    # os.environ['WECHATY_PUPPET_SERVICE_TOKEN']='test01'
    # os.environ['WECHATY_PUPPET']='wechaty-puppet-xp'
    # os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT']='127.0.0.1:8080'

    # os.environ['WECHATY_PUPPET_SERVICE_NO_TLS_INSECURE_SERVER']='true'
    # os.environ['WECHATY_PUPPET_SERVICE_NO_TLS_INSECURE_CLIENT']='true'

    bot = Wechaty()

    bot.on('scan',      on_scan)
    bot.on('login',     on_login)
    bot.on('message',   on_message)

    await bot.start()

    print('[Python Wechaty] Ding Dong Bot started.')


asyncio.run(main())