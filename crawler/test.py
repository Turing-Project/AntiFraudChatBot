import json
import requests
from decimal import Decimal
import pprint
headers ={
    'referer': 'https://www.bilibili.com/video/BV1t3411p7Vq?spm_id_from=444.41.0.0',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53',
}
main_url = 'https://api.bilibili.com/x/v2/reply/main?'
main_params = {
    'jsonp': 'jsonp',
    'next': 1,
    'type': '1',
    'oid': '425009881',
    'mode': '3',
    'plat': '1',
    '_': '1648289436898'
}
reply_url = 'https://api.bilibili.com/x/v2/reply/reply'
reply_params = {
    'jsonp': 'jsonp',
    'pn': '1',
    'type': '1',
    'oid': '425009881',
    'ps': '100',
    'root': '106841868432',
    '_': '1648290346968'
}
proxies={
    'http':'20.24.65.59:6655'
}
dic = {}
dic['count'] = Decimal('0')
#楼中楼
def parse_reply(root,ps,count):
    reply_params['root'] = root
    reply_params['ps'] = ps
    response = requests.get(url=reply_url, headers=headers, params=reply_params)
    page_text_json = response.json()
    for comment in page_text_json['data']['replies']:
        dic['count'] += Decimal('0.0001')
        dic['username'] = comment['member']['uname']
        dic['content'] = comment['content']['message']
        dic['like_count'] = comment['like']
        print(dic)
        f.write(str(dic['count']) + str(dic['username']) + str(dic['content']) + str(dic['like_count']) + '\n')
    dic['count'] = count
#评论楼层
def parse_main_reply():
    response = requests.get(url = main_url, headers = headers,params = main_params)
    page_text = response.text
    page_text_json = response.json()
    with open('test.html','w',encoding='utf-8') as fp:
        fp.write(page_text)
    fp.close()
    if page_text_json['data']['cursor']['is_end'] == False:
        for comment in page_text_json['data']['replies']:
            dic['count'] += Decimal('1')
            dic['username'] = comment['member']['uname']
            dic['content'] = comment['content']['message']
            dic['reply_count'] = comment['rcount']
            dic['reply_id'] = comment['rpid']
            dic['like_count'] = comment['like']
            dic['total_reply_num'] = page_text_json['data']['cursor']['all_count']
            dic['is_end'] = page_text_json['data']['cursor']['is_end']
            print(dic)
            f.write(str(dic['count'])+str(dic['username'])+str(dic['content'])+str(dic['reply_count'])+str(dic['reply_id'])+str(dic['like_count'])+str(dic['total_reply_num'])+str(dic['is_end'])+'\n')
            if dic['reply_count'] != 0:
                parse_reply(dic['reply_id'],dic['reply_count'],dic['count'])
        main_params['next'] += 1
        return parse_main_reply()
    elif page_text_json['data']['cursor']['is_end'] == True:
        print('结束')
f = open('test.txt','a',encoding='utf-8')
parse_main_reply()
f.close()