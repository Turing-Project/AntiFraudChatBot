from utils.requester import request
def download_segment(url):
    headers = {
        'accept': '*/*',
    'accept-encoding': 'identity',
    'accept-language': 'zh-CN,zh;q=0.9',
    'if-range': 'Thu, 22 Jul 2021 09:43:08 GMT',
    'origin': 'https://www.bilibili.com',
    'range': 'bytes=0-1995353',
    'referer': 'https://www.bilibili.com/video/BV1XL411H79r',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    }
    # url='https://xy121x31x142x181xy.mcdn.bilivideo.cn:4483/upgcxcode/56/25/374632556/374632556_nb2-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1626969237&gen=playurlv2&os=mcdn&oi=1885373441&trid=000191f5b7d25fed4e63bbd80e017001bc64u&platform=pc&upsig=e74d310419272cfdb787edfcf3a9434c&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mcdnid=9000626&mid=23064683&bvc=vod&nettype=0&orderid=0,3&agrr=0&logo=A0000100'

    # url2 = 'https://xy171x39x15x196xy.mcdn.bilivideo.cn:4483/upgcxcode/56/25/374632556/374632556_nb2-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1627038912&gen=playurlv2&os=mcdn&oi=1885389723&trid=0001d1522260ac414b16bf9a5541b8578eb0u&platform=pc&upsig=356be02417e4af1928ec3d264bb8f943&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mcdnid=9000723&mid=28697381&bvc=vod&nettype=0&orderid=0,3&agrr=1&logo=A000010'

    content = request(url, headers=headers)
    return content





# quit()
# with open('test.m4s', 'wb') as f:
#     f.write(c)
#     f.close()

