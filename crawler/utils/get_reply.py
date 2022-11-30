# coding:utf8
import requests


def get_raw_reply(aid):
    headers = {
    'accept': '*/*',
    # 'accept-encoding': 'gzip, deflate, br',
    'accept-encoding': 'deflate',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    # 'cookie': 'pgv_pvi=300764160; rpdid=olwwwliplodosoqqwokww; _uuid=EA9827E7-550F-BFB8-CA1B-8257DCDC960468224infoc; buvid3=93A293B0-2EAC-4F96-87BB-E7D398CBCC57148797infoc; CURRENT_FNVAL=80; blackside_state=1; fingerprint=bc56ed3fa67484bb54a6f2c0d34d101f; buvid_fp=93A293B0-2EAC-4F96-87BB-E7D398CBCC57148797infoc; buvid_fp_plain=93A293B0-2EAC-4F96-87BB-E7D398CBCC57148797infoc; SESSDATA=d82262f7%2C1642232589%2Cee061%2A71; bili_jct=bfba5357d0ca1966160cce82a70380b7; DedeUserID=23064683; DedeUserID__ckMd5=864e26ed3b2a0940; sid=56yroqa6; CURRENT_QUALITY=80; PVID=1; bfe_id=5db70a86bd1cbe8a88817507134f7bb5',
    'pragma': 'no-cache',
    # 'referer': 'https://www.bilibili.com/video/BV1XL411H79r',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    }
    page = 0
    reply_lst = []
    while True:
        assert aid.isdigit(), 'aid is not digit'
        url = 'https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={}&type=1&oid={}&mode=3&plat=1&'.format(page, aid)
        # url = 'https://api.bilibili.com/x/v2/reply/main?callback=jQuery17207723215742327245_1627299231613&jsonp=jsonp&next=7&type=1&oid=461774991&mode=3&plat=1&_=1627299537026'
        req = requests.get(url, headers=headers)
        req.encoding = req.apparent_encoding
        # print(req.content.decode('utf8'))
        content = req.content.decode('utf8')
        json = content.replace('null', 'None').replace('true', 'True').replace('false', 'False')
        json = eval(json)
        # print(json)
        if json["data"]['cursor']['is_end']:
            break
        reply_lst.append(json)
        page += 1

        # print(reply_lst)
    return reply_lst


if __name__ == '__main__':

    # print(get_raw_reply('461774991'))
    # print(get_raw_reply('461774991'))
    print(get_raw_reply('360863614'))

