import urllib3
import json
import os
import logging


class RasaIntent:
    """
    @基于rasa的通用intent意图识别
    @参考https://github.com/bigbrother666sh/Awada
    """
    def __init__(
            self,
            logs: str = '.utils',
            port: str = '5005',
    ) -> None:
        # 1. create the cache_dir
        self.cache_dir = logs
        os.makedirs(self.cache_dir, exist_ok=True)

        # 2. save the log info into <plugin_name>.log file
        log_formatter = logging.Formatter(fmt='%(levelname)s - %(message)s')
        self.logger = logging.getLogger('rasaintent')
        self.logger.handlers = []
        self.logger.setLevel('INFO')
        self.logger.propagate = False
        log_file = os.path.join(self.cache_dir, 'intent_LTE.log')

        file_handler = logging.FileHandler(log_file, 'a', encoding='utf-8')
        file_handler.setLevel('INFO')
        file_handler.setFormatter(log_formatter)
        self.logger.addHandler(file_handler)

        # 3. create the http client
        self.http = urllib3.PoolManager()

        # 4. create the rasa url
        self.url = 'http://localhost:' + port + '/parse'

        # 3. create the http client
        self.rasa_url = 'http://localhost:'+port+'/model/parse'
        self.http = urllib3.PoolManager()

        _test_data = {'text': '我想邀请你一起投资'}
        _encoded_data = json.dumps(_test_data)
        _test_res = self.http.request('POST', self.rasa_url, body=_encoded_data)
        _result = json.loads(_test_res.data)

        if not _result:
            raise RuntimeError('Rasa server not running, pls start it first and trans the right port in str')

    def predict(self, text: str):
        _test_data = {'text': text}
        _encoded_data = json.dumps(_test_data)
        _test_res = self.http.request('POST', self.rasa_url, body=_encoded_data)
        _result = json.loads(_test_res.data)
        _intent = _result['intent']['name']
        _conf = _result['intent']['confidence']
        if _conf >= 0.5 and _intent != 'nlu_fallback':
            self.logger.info(f'text: {text}---Intent: {_intent} confidence: {_conf}')
        else:
            self.logger.warning(f'text: {text}---Intent: {_intent} confidence: {_conf}')
        return _intent, _conf


if __name__ == "__main__":
    nlu_intent = RasaIntent()
    print("====意图测试====")

    while True:
        print("输入Q退出")
        prompt = input("输入待测文本：")
        if prompt.lower() == "q":
            break
        intent, conf = nlu_intent.predict(prompt)
        print("检测出意图：", intent)
        print("意图置信度：", conf)