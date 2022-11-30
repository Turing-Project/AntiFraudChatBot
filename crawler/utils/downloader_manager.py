from utils.requester import request
from utils.seg_downloader import download_segment
from utils.get_video_html import get_video_html
from utils.logger import logger
from utils.get_reply import get_raw_reply
from tqdm import tqdm
import os
import time
import random
import sys
import pickle
import requests
from concurrent.futures import ThreadPoolExecutor
import os

def segment(url, idx, path, type): # v a
    if os.path.exists('{}/{}_{}.m4s'.format(path, type, idx)) and os.path.getsize('{}/{}_{}.m4s'.format(path, type, idx)) > 100:
        return True
    content = download_segment(url)
    with open('{}/{}_{}.m4s'.format(path, type, idx), 'wb') as f:
        f.write(content)
        f.close()
    return True

def make_headers(lower, upper):
    return {
        'accept': '*/*',
        'accept-encoding': 'identity',
        'accept-language': 'zh-CN,zh;q=0.9',
        'if-range': 'Thu, 22 Jul 2021 09:43:08 GMT',
        'origin': 'https://www.bilibili.com',
        'range': 'bytes={}-{}'.format(lower, upper),
        'referer': 'https://www.bilibili.com/video/BV1XL411H79r',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    }

def get_dm(cid):
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'cache-control': 'no-cache',
# 'cookie': "buvid3=9E1A6A86-CB00-5318-15FB-903621F0E7EA13898infoc; _uuid=7BF9C0C8-1DC4-E762-BBC5-5FF8B6717E5317552infoc; sid=6yx7ol6r; rpdid=|(umlmkklkJ~0J'uYk~ukk~RR; CURRENT_FNVAL=80; blackside_state=1; PVID=1",
'pragma': 'no-cache',
'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
'sec-ch-ua-mobile': '?1',
'sec-fetch-dest': 'document',
'sec-fetch-mode': 'navigate',
'sec-fetch-site': 'none',
'sec-fetch-user': '?1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36'}
    dm_xml = request('https://comment.bilibili.com/{}.xml'.format(cid), headers=headers)
    return dm_xml.decode('utf8')



def save_info(path, info_d):
    with open('{}/info.json'.format(path), 'w') as f:
        for i in info_d:
            f.write('{}:{}\n'.format(i, info_d[i]))
    dm = get_dm(info_d['cid'])
    with open('{}/dm.xml'.format(path), 'w') as f:
        f.write(dm)
    return

def save_reply(path, aid):
    reply_d = get_raw_reply(aid)
    pickle.dump(reply_d, open('{}/replay.pkl'.format(path), 'wb'))
    return

def save_cover(path, curl):
    req = requests.get(curl, headers= {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'})
    with open('{}/cover.jpg'.format(path), 'wb') as f:
        f.write(req.content)
    return

def single_video(bv, location):

    va, v_info = get_video_html(bv)
    # print(v_info)
    videos, audios = va
    start_length = 0
    v_length_offset = 2000000
    a_length_offset = 200000

    title = v_info['title']
    author = v_info['author']
    folder_name = '{}-{}'.format(author, title)
    path = '{}/{}'.format(location, folder_name)
    if not os.path.exists(location):
        os.mkdir(location)
    if not os.path.exists(path):
        os.mkdir(path)

    logger(path, type='path')
    # quit()
    # print(videos, audios)
    response_length = 1
    idx=0
    print('[Videos]:', end='')
    while response_length >= 1:
        # try:
            headers = make_headers(lower=start_length, upper=start_length+v_length_offset)
            # print(headers)
            content = requests.get(videos, headers=headers)
            # print(content.headers)
            recv_length = int(content.headers['Content-Length'])
            start_length += recv_length

            with open('{}/{}_{}.m4s'.format(path, 'v', idx), 'wb') as f:
                f.write(content.content)
                f.close()
            judge = [int(i) for i in str(content.headers['Content-Range']).split(' ')[1].split('-')[1].split('/')]
            if judge[1]-judge[0]==1 or sys.getsizeof(content.content)<50:
                break
            else:
                idx += 1
            print('##', end='')

        # except:
        #     pass

    # quit()
    print('')
    print('[Audios]:', end='')
    start_length = 0
    idx_a = 0

    while response_length >= 1:
        # try:
            headers = make_headers(lower=start_length, upper=start_length+a_length_offset)
            # print(headers)

            content = requests.get(audios, headers=headers)
            # print(content.headers)
            recv_length = int(content.headers['Content-Length'])
            start_length += recv_length

            with open('{}/{}_{}.m4s'.format(path, 'a', idx_a), 'wb') as f:
                f.write(content.content)
                f.close()
            judge = [int(i) for i in str(content.headers['Content-Range']).split(' ')[1].split('-')[1].split('/')]
            if judge[1]-judge[0]==1:
                break
            else:
                idx_a += 1
            print('##', end='')

    print('')


    merge(path, idx, idx_a)
    clean(path, idx, idx_a)
    save_info(path, info_d=v_info)
    save_reply(path, aid=v_info['aid'])
    save_cover(path, curl=v_info['curl'])

    # import requests
    #
    # content = requests.get(videos, headers = {
    #     'accept': '*/*',
    # 'accept-encoding': 'identity',
    # 'accept-language': 'zh-CN,zh;q=0.9',
    # 'if-range': 'Thu, 22 Jul 2021 09:43:08 GMT',
    # 'origin': 'https://www.bilibili.com',
    # 'range': 'bytes=0-2000000',
    # 'referer': 'https://www.bilibili.com/video/BV1XL411H79r',
    # 'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-fetch-dest': 'empty',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'cross-site',
    # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    # })
    #
    # print(content.content)
    # # print(content.status_code)
    # print(content.headers)
    # with open('v.m4s', 'wb') as f:
    #     f.write(content.content)
    #
    # content = requests.get(audios, headers={
    #     'accept': '*/*',
    #     'accept-encoding': 'identity',
    #     'accept-language': 'zh-CN,zh;q=0.9',
    #     'if-range': 'Thu, 22 Jul 2021 09:43:08 GMT',
    #     'origin': 'https://www.bilibili.com',
    #     'range': 'bytes=0-200000',
    #     'referer': 'https://www.bilibili.com/video/BV1XL411H79r',
    #     'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-site': 'cross-site',
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
    # })
    #
    # with open('a.m4s', 'wb') as f:
    #     f.write(content.content)
    # quit()

    # tp = ThreadPoolExecutor(workers)
    # status_lst_v = []
    # status_lst_a = []
    # total_idx_v = 0
    # total_idx_a = 0
    # for idx_v in tqdm(range(len(videos))):
    #     ret = tp.submit(segment, url=videos[idx_v]['url'], idx=idx_v, path=path, type='v')
    #     status_lst_v.append(ret)
    #     total_idx_v = idx_v
    #
    # for idx_a in tqdm(range(len(audios))):
    #     ret = tp.submit(segment, url=videos[idx_a]['url'], idx=idx_a, path=path, type='a')
    #     status_lst_a.append(ret)
    #     total_idx_a = idx_a
def merge(path, total_idx_v, total_idx_a):
    with open('{}/video.m4s'.format(path), 'ab') as vo:
        for idx in range(total_idx_v+1):
            vo.write(open('{}/v_{}.m4s'.format(path, idx), 'rb').read())
        vo.close()

    with open('{}/audio.m4s'.format(path), 'ab') as vo:
        for idx in range(total_idx_a+1):
            vo.write(open('{}/a_{}.m4s'.format(path, idx), 'rb').read())
        vo.close()
    cmd = """cd "{}";ffmpeg -i "video.m4s" -i "audio.m4s" -codec copy "output.mp4" -y;cd -;""".format(path)
    # print(cmd)
    os.system(cmd)
    # os.popen("""cd {};ffmpeg -i video.m4s -i audio.m4s -codec copy out.mp4;cd -;""".format(path))

def clean(path, total_idx_v, total_idx_a):
    os.remove('{}/audio.m4s'.format(path))
    os.remove('{}/video.m4s'.format(path))
    for idx in range(total_idx_v + 1):
        os.remove('{}/{}_{}.m4s'.format(path, 'v', idx))
    for idx in range(total_idx_a + 1):
        os.remove('{}/{}_{}.m4s'.format(path, 'a', idx))

def executor(video_lst, location, workers=3):
    tp = ThreadPoolExecutor(workers)
    for bv in tqdm(video_lst):
        tp.submit(single_video, bv, location)









if __name__ == '__main__':

    # single_video('BV1XL411H79r', location='temp')
    # single_video('BV1aW411D7cG', location='temp')
    # https://www.bilibili.com/video/BV1wt411v75C/
    # single_video('BV13K4y1v7yg', location='.')
    # single_video('BV1wt411v75C', location='temp')
    # merge('temp/【西瓜新】千里邀月☾是谁的真情感动上天-西瓜新', 10, 0)
    # get_dm(52851657)
    # single_video('BV1hK4y1g74B', location='temp')
    # BV1bU4y1t72q
    # single_video('BV1g441157ob', location='temp')
    # executor(['BV1wq4y1p7Um'], location='temp')
    executor(['BV1vK411K7Yj'], location='temp')


