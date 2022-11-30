import re
from utils.logger import logger
from utils.requester import request


def get_video_html(bv):

    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': 'pgv_pvi=300764160; rpdid=olwwwliplodosoqqwokww; PVID=1; _uuid=EA9827E7-550F-BFB8-CA1B-8257DCDC960468224infoc; buvid3=93A293B0-2EAC-4F96-87BB-E7D398CBCC57148797infoc; CURRENT_FNVAL=80; blackside_state=1; fingerprint=bc56ed3fa67484bb54a6f2c0d34d101f; buvid_fp=93A293B0-2EAC-4F96-87BB-E7D398CBCC57148797infoc; buvid_fp_plain=93A293B0-2EAC-4F96-87BB-E7D398CBCC57148797infoc; SESSDATA=d82262f7%2C1642232589%2Cee061%2A71; bili_jct=bfba5357d0ca1966160cce82a70380b7; DedeUserID=23064683; DedeUserID__ckMd5=864e26ed3b2a0940; sid=56yroqa6; CURRENT_QUALITY=80',
    'cooke': "fingerprint=0c504bdc7b1df5414344af0cc0257aee; buvid_fp=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; buvid_fp_plain=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; buvid3=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; _uuid=45F1ECFC-CF41-5057-7B0F-A98059E33DF741329infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(u))lJm~J)u0J'uYk~JYu)mm; buvid_fp=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; buvid_fp_plain=2CD0AEF0-B134-3D0E-2811-B8761ABC5C6439485infoc; PVID=1; fingerprint=64607ea7a5c07362b82455c1891e6854; SESSDATA=18b6f789%2C1643136218%2C275a8%2A71; bili_jct=55b60adb00c225ad43afada35b81a391; DedeUserID=28697381; DedeUserID__ckMd5=071ff1fa313dce25; sid=bisg808v",
    # 'cookie': """fpgv_pvi=300764160; rpdid=olwwwliplodosoqqwokww; _uuid=EA9827E7-550F-BFB8-CA1B-8257DCDC960468224infoc; buvid3=93A293B0-2EAC-4F96-87BB-E7D398CBCC57148797infoc; CURRENT_FNVAL=80; blackside_state=1; fingerprint=bc56ed3fa67484bb54a6f2c0d34d101f; buvid_fp=93A293B0-2EAC-4F96-87BB-E7D398CBCC57148797infoc; buvid_fp_plain=93A293B0-2EAC-4F96-87BB-E7D398CBCC57148797infoc; SESSDATA=d82262f7%2C1642232589%2Cee061%2A71; bili_jct=bfba5357d0ca1966160cce82a70380b7; DedeUserID=23064683; DedeUserID__ckMd5=864e26ed3b2a0940; sid=56yroqa6; CURRENT_QUALITY=80; PVID=2""",
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}

#     headers = {
#
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
# 'accept-encoding': 'gzip, deflate, br',
# 'accept-language': 'zh-CN,zh;q=0.9',
# 'cache-control': 'no-cache',
# 'cookie': 'pgv_pvi=300764160; rpdid=olwwwliplodosoqqwokww; _uuid=EA9827E7-550F-BFB8-CA1B-8257DCDC960468224infoc; buvid3=93A293B0-2EAC-4F96-87BB-E7D398CBCC57148797infoc; CURRENT_FNVAL=80; blackside_state=1; fingerprint=bc56ed3fa67484bb54a6f2c0d34d101f; buvid_fp=93A293B0-2EAC-4F96-87BB-E7D398CBCC57148797infoc; buvid_fp_plain=93A293B0-2EAC-4F96-87BB-E7D398CBCC57148797infoc; SESSDATA=d82262f7%2C1642232589%2Cee061%2A71; bili_jct=bfba5357d0ca1966160cce82a70380b7; DedeUserID=23064683; DedeUserID__ckMd5=864e26ed3b2a0940; sid=56yroqa6; CURRENT_QUALITY=80; PVID=2',
# 'pragma': 'no-cache',
# 'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
# 'sec-ch-ua-mobile': '?0',
# 'sec-fetch-dest': 'document',
# 'sec-fetch-mode': 'navigate',
# 'sec-fetch-site': 'none',
# 'sec-fetch-user': '?1',
# 'upgrade-insecure-requests': '1',
# 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
#     }

    base_url = 'https://www.bilibili.com/video/{}'.format(bv)
    logger('target: [{}]'.format(base_url))
    content = request(url=base_url, headers=headers)
    # print(content)
    m3u8_dict, v_info = parse_html(content, bv=bv)
    aid = parse_aid(content)
    aid = str(aid)[2:-1]
    # print(m3u8_dict)
    videos = m3u8_dict['data']['dash']['video']
    audios = m3u8_dict['data']['dash']['audio']
    # print(videos, audios)
    # print(len(videos), len(audios))

    headers = {
        'pragma': 'no-cache',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?1',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'}
    content = request(base_url, headers=headers)
    cid = parse_cid(content)
    # print(cid)
    # quit()
    v_info['cid'] = cid
    v_info['aid'] = aid

    cover_url = parse_cover_url(content)
    # print(cover_url)
    v_info['curl'] = cover_url
    # print(aid)

    return make_tasks(videos, audios), v_info


def parse_cid(content):
    rule_cid = re.compile(b"""window\.videoCid =.*?</script>""", re.S)
    cid = rule_cid.findall(content)
    cid = str(cid).split('= ')[1].split('\\n')[0]
    return cid

def parse_aid(content):
    # print(content.decode('utf8'))
    rule_aid = re.compile(b'window.__INITIAL_STATE__={"aid":(.*?),"bvid":".*?","p":1,"episod', re.S)
    # content = b'window.__INITIAL_STATE__={"aid":888867658,"bvid":"BV1hK4y1g74B","p":1,"episode":"","vi'
    aid = rule_aid.findall(content)[0]
    # print(aid)
    # quit()
    return aid

def parse_cover_url(content):
    rule_cover = re.compile(b'<meta data-vue-meta="true" itemprop="image" content="(.*?)"><meta data-vue-meta="true" ', re.S)
    cover_url = rule_cover.findall(content)[0]
    return cover_url

def save_title(title):
    title = str(title).replace('/', '-').replace('\\', '-').replace('(', '（').replace(')', '）').replace(' ', '_')
    return title


def parse_html(content, bv):
    relu = re.compile(b'<script>window.__playinfo__=(.*?)</script><script>', re.S)
    match_dict = relu.findall(content)
    # print(match_dict[0])
    # print(type(match_dict[0]))

    rule_title = re.compile(b'<span class="tit tr-fix">(.*?)</span>', re.S)
    rule_title_2 = re.compile(b'<span class="tit">(.*?)</span>', re.S)
    rule_count_play = re.compile(b'<span title="(.*?)" class="view">', re.S)
    rule_time = re.compile(b'</span><span>(.*?)</span><!----></div></div>', re.S)
    rule_count_like = re.compile(b't-scroll-module"><div class="ops"><!----><!----><!----><!----><span title="(.*?)" class="like"><!----><!----><!----><!----><i class="van-icon-videodetails_like"></i>', re.S)
    rule_count_star = re.compile(b"""</canvas><!----><i class="van-icon-videodetails_collec" style="color:;"></i>(.*?)
    </span><span title=".*?" class="share"><i class="van-icon-videodetails_share">""", re.S)
    rule_count_dammu = re.compile(b'class="view">.*?</span><span title=".*?" class="dm">(.*?)</span><span', re.S)
    rule_des = re.compile(b'<meta data-vue-meta="true" itemprop="description" name="description" content="(.*?)">', re.S)
    rule_author = re.compile(b'<meta data-vue-meta="true" itemprop="author" name="author" content="(.*?)">', re.S)


    try:
        title = rule_title.findall(content)[0]
        title = title.decode('utf8')
    except:
        try:
            title = rule_title_2.findall(content)[0]
            title = title.decode('utf8')
        except:
            title = bv
    try:
        play = rule_count_play.findall(content)[0]
        play = play.decode('utf8')
    except:
        play = None
    try:
        time = rule_time.findall(content)[0]
        time = time.decode('utf8')
    except:
        time = None
    try:
        like = rule_count_like.findall(content)[0]
        like = like.decode('utf8')
    except:
        like = None
    try:
        star = rule_count_star.findall(content)[0]
        star = star.decode('utf8')
    except:
        star = None
    try:
        description = rule_des.findall(content)[0]
        description = description.decode('utf8')
    except:
        description = None
    try:
        author = rule_author.findall(content)[0]
        author = author.decode('utf8')
    except:
        author = None
    try:
        damaku = rule_count_dammu.findall(content)[0]
        damaku = damaku.decode('utf8')
    except:
        damaku = None
    title = save_title(title)


    return eval(str(match_dict[0], encoding='utf8').replace('null', 'None')), {'title':title, 'play':play, 'time':time, 'like':like, 'star':star, 'description':description, 'author':author, 'dammu':damaku}



def make_tasks(videos, audios):
    # videos_tasks = []
    # audios_tasks = []
    # for item in videos:
    #     videos_tasks.append({'url':item['base_url'], 'range':item['segment_base']['index_range']})

    # for item in audios:
    #     audios_tasks.append({'url': item['base_url'], 'range': item['segment_base']['index_range']})


    # print(videos_tasks, audios_tasks)

    # for i in videos_tasks:
    #     print(i)
    # quit()
    video_url = videos[0]['baseUrl']
    audio_url = audios[0]['baseUrl']
    # return videos_tasks, audios_tasks
    return video_url, audio_url








if __name__ == '__main__':

    get_video_html('BV1XL411H79r')
