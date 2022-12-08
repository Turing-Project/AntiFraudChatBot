"""
Licensed under the Apache License, Version 2.0 (the 'License');
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an 'AS IS' BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
                                            2022 @ Copyright revised
"""
from typing import Any

from wechaty import (
    Contact,
    Message,
    Wechaty,
    MessageType,
    ScanStatus
)
import os, sys, time, datetime
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import json
import asyncio
import emoji
import paddlehub as hub
from urllib.parse import quote
from inspurai import Yuan, set_yuan_account, Example

sys.path.append(os.path.abspath(os.curdir))


class AntifraudBotBuilder(object):
    """
    Author: Turing's Cat 2022/08/22
    @:param ->
            data,model,msg::str

    References:
    Python Wechaty - https://github.com/wechaty/python-wechaty-getting-started/
    Yuan1.0 API - https://github.com/Shawn-Inspur/Yuan-1.0
    Paddlehub - https://github.com/PaddlePaddle/PaddleHub
    AI Jubensha - https://github.com/bigbrother666sh/shezhangbujianle
    """

    def __init__(self):
        self.data = None
        self.hold = None
        self.persona = None
        self.statement = "你好~在使用此AI前需要声明：
                         "\n1.当前对话不涉及任何隐私信息，双方共同确认对话的可公开性，\n" \
                         "2.对话过程中请勿讨论敏感话题，否则需自行承担不当言论可能造成的法律风险。\n" \
                         "3.如不接受请即刻停止对话，继续对话将被视为完全理解并接受上述声明。"
        self.memory_len = 2 << 5
        self.memory_step = 0
        self.memory = {}
        self.context = {}
        self.simnet_bow = hub.Module(name="simnet_bow")
        self.bad_detection = hub.Module(name="porn_detection_lstm")
        self.temperature = 0.95

    def parse_data(self, input_file):
        """
        parse the example-reply data for AI dialog
        :param input_file:
        """
        with open(input_file, 'r', encoding='utf-8') as f:
            self.data = [line for line in f.readlines() if line.strip()]
            print("examples loaded successfully")

    def parse_split(self, input_file, split):
        """
        parse the example-reply data for AI dialog
        :param ->
                input_file, floag:
        """
        if split:
            with open(input_file, 'r', encoding='utf-8') as f:
                self.hold = f.read()

    def set_persona(self, bot_context):
        """
        AI profile setting according to pre-defined personal inf.
        :param bot_context:
        """
        with open(bot_context, 'r', encoding='utf-8') as f:
            self.persona = f.read()
            print("bot_info loaded successfully")


    @staticmethod
    def dialog_dict(self, text, user_id) -> str:
        """
        @:param ->
                    text=str, id=long
        @:description-- static(temp_) for test
        """
        answer_list = {}
        answer = ""
        memory = ""
        answer_key = []
        memory_key = []
        key = False
        for i in range(0, len(self.data), 2):
            if i + 1 >= len(self.data):
                break
            answer_list[self.data[i].strip('\n')] = self.data[i+1].strip('\n')
            answer_key.append(text
                              .replace("~", "")
                              .replace("？", "")
                              .replace("！", ""))

        sim_list = [list(answer_list.keys()), answer_key[:]]
        results = self.simnet_bow.similarity(texts=sim_list, use_gpu=True)
        results.sort(key=lambda k: (k.get('similarity')), reverse=True)

        # 计算短期记忆库的匹配度，获取topk条记忆
        for memory_chat in self.memory[user_id][:-1]:
            if text in memory_chat:
                memory = memory_chat
                key = True
            memory_key.append(memory_chat)

        if not key and len(memory_key) > 0:
            answer_key = answer_key[:len(memory_key)]
            memory_list = [[sentence.split("：")[1] for sentence in memory_key], answer_key[:len(memory_key)]]
            try:
                results = self.simnet_bow.similarity(texts=memory_list, use_gpu=True)
            except Exception:
                return AntifraudBotBuilder.dialog_core(self, text, user_id)
            results.sort(key=lambda k: (k.get('similarity')), reverse=True)
            memory = results[0]

        if memory != "":
            pass
            # text = memory + "。对话：" +  text #todo

        for result in results:
            # 计算与example库的相似度，读取prompt
            if result['similarity'] >= 0.9:
                print("example match---current dialog：", result['text_1'],
                      "|memorized in  window ", str(self.memory_step))
                answer = answer_list[result['text_1']]
                time.sleep(5 * len(answer) / 10)
                break
                # print("example load---similarity：", result['similarity'])
            else:
                answer = AntifraudBotBuilder.dialog_core(self, text, user_id)
                if answer != "":
                    break
                else:
                    break

        return answer

    @staticmethod
    def dialog_core(self, text, usr_id) -> Any:
        yuan = Yuan(engine='dialog',
                    input_prefix="对话：“",
                    input_suffix="”",
                    output_prefix="水思源：“",
                    output_suffix="”",
                    append_output_prefix_to_query=True)
        test_text_1 = []
        test_text_2 = []

        for i in range(0, len(self.data), 2):
            test_text_1.append(self.data[i].strip('\n'))
            test_text_2.append(text)

        test_text = [test_text_1, test_text_2]
        results = self.simnet_bow.similarity(texts=test_text, use_gpu=True)
        results.sort(key=lambda k: (k.get('similarity')), reverse=True)

        yuan.temperature = self.temperature
        yuan.add_example(Example(inp=self.persona, out="\n"))
        # print(f"the temperature is:{yuan.get_temperature()} \n")

        for result in results:# 计算与example库种prompt的相似度，读取上下文context
            if result['similarity'] >= 0.85:
                yuan.add_example(
                    Example(inp=result['text_1'],
                            out=self.data[self.data.index(result['text_1'] + '\n') + 1].strip('\n')))
                print("example prompt---current dialog：", result['text_1'], "memorized")
            else:
                break

        if len(yuan.examples) == 0:
            print("no suitable example found---top-3 context：", results[0]['similarity'], "，",
                  results[1]['similarity'], "，",
                  results[2]['similarity'])

        while (1):
            time.sleep(1)
            try:
                reply = yuan.submit_API(text, trun="”")
            # reply = yuan.submit_API(''.join(self.memory[usr_id])[4:], trun="”") 开启强制记忆机制
            except Exception:
                break
            if len(self.memory[usr_id]) > 0 and reply != self.memory[usr_id][-1][4:-1]:
                if len(self.memory[usr_id]) > 1:
                    if reply != self.memory[usr_id][-2][3:-1]:
                        break
                else:
                    break

        date = datetime.date.today().strftime("%d_%m_%Y")
        with open(date + ".txt", 'a', encoding='utf-8') as f:
            f.write("Q:" + text + "---top-3 similarity：" + str(results[0]['similarity']) + "，" + str(
                results[1]['similarity']) + "，" + str(results[2]['similarity']) + "\n")
            f.write(reply + "\n")
        return reply

    def combine_multi_dialog(self) -> boolean:
        """
        部分功能还在调试，暂不开源
        """
        return
    
    async def on_message(self, msg: Message):
        """
        Message Handler for the Bot
        """
        global rooms

        # 暂不支持语音读取（wechaty最新版可以支持语音转文字功能，后续待升级）
        if msg.type() == MessageType.MESSAGE_TYPE_AUDIO:
            await msg.say("不好意思啊我现在不方便听语音，可以打字吗")

        if msg.is_self() or msg.type() != MessageType.MESSAGE_TYPE_TEXT:
            return

        talker = msg.talker()
        text = msg.text()
        id = talker.contact_id

        if "emoji" in text or "emoti" in text:# 暂时无法识别表情包
            return

        if text == '以上是打招呼的内容':
            await talker.say(self.statement)
            return

        if text == '1':
            with open('rooms.json', 'w') as f:
                json.dump(rooms, f)
            print("rooms dict has been saved as bigbro/rooms.jason")
            return

        if text in self.hold or text[1:] in self.hold:
            return

        #根据时间窗口将多轮对话合并成一句
        self.combine_multi_dialog()
        
        text = text.replace(r'\s', "，").replace("#", "号").replace("&", "和")
        # bad_detection_result = self.bad_detection.detection(texts=[text], use_gpu=True, batch_size=1)
        #
        # if bad_detection_result[0]['porn_detection_label'] == 1:
        #     await msg.say("请勿发表不当言论，您需要对您的言行负全部法律责任")
        #     return

        if id not in self.memory.keys(): # 第一次对话时声明（上线可以注释掉）
            self.memory[id] = []
            # await talker.say(self.statement)
            # return
        else:
            if len(self.memory[id]) > self.memory_len:  # 记忆过去N轮对话中对方说的句子
                self.memory[id].pop(0)
            self.memory[id].append("对话：“" + text + "”")

        # emoj = emoji.core.emoji_lis("chinese")
        # print(f'emoji list has set as{emoj} \n')

        if len(self.memory[id]) < 2 and ("好的" in text or "OK" in text):
            reply = "[OK]收到"
        else:
            reply = AntifraudBotBuilder.dialog_dict(self, text, id)

        # 对通用的字符，比如[可爱][哭泣]替换为emoji
        reply = emoji.emojize(reply)
        if reply:
            await talker.say(reply)

        if len(self.memory[id]) > self.memory_len:
            self.memory[id].pop(0)
        self.memory[id].append("水思源：“" + reply + "”")
        if self.memory_step > self.memory_len:
            self.memory_step = 0
        else:
            self.memory_step += 1

    async def on_login(user: Contact):
        """
        Login Handler for the Bot
        """
        print(user)

    async def on_scan(
            qrcode: str,
            status: ScanStatus,
            _data,):
        """
        Scan Handler for the Bot
        """
        print('Status: ' + str(status))
        print('View QR Code Online: https://wechaty.js.org/qrcode/' + quote(qrcode))


async def main():
    """
    Async Main Entry
    """

    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')
    #for cloud-service
    os.environ['WECHATY_PUPPET_SERVICE_TOKEN']='your_token'
    os.environ['WECHATY_PUPPET']='wechaty-puppet-padlocal'
    os.environ['WECHATY_PUPPET_SERVICE_ENDPOINT']='your_ip'

    bot = Wechaty()
    core = AntifraudBotBuilder()
    core.parse_data("./prompt/bot_example.txt")
    core.parse_split('./prompt/split.txt', True)

    set_yuan_account("turingscat", "your_account")
    core.set_persona("./prompt/bot_info.txt")

    bot.on('scan',  core.on_scan)
    bot.on('login', core.on_login)
    bot.on('message', core.on_message)
    # bot.on('friendship', on_request)

    await bot.start()

    print('[Python Wechaty] Anti-fraud Bot has been started.')


if __name__ == "__main__":
    asyncio.run(main())
