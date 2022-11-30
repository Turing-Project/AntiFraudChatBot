from utils.logger import logger, err_logger
from utils.auto_utils import AutoUtils
from utils.findauthor import run
from utils.downloader_manager import executor, single_video

import os
import argparse
from tqdm import tqdm

class GreenSystem:
    __doc__ = """
    用于下载B站视频or评论，从命令行获取要被爬取的up（可以遍历也可以指定）
    启动后，将不停地爬取数据库中的视频
    """

    def __init__(self, db_path, user_dy_path, video_down_path):
        self.db_path = db_path
        self.user_dy_path = user_dy_path
        self.video_down_path = video_down_path
        self.check_dirs()
        self.findauthor = run
        self.auto_utils = AutoUtils(db_path=self.db_path)

    @staticmethod
    def make_dirs(path):
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    def check_dirs(self):
        self.make_dirs(self.user_dy_path)
        self.make_dirs(self.video_down_path)

    def run(self):
        while True:
            bvid = self.auto_utils.get_one_vid()
            # executor([bvid,], location=self.video_down_path)
            single_video(bvid, location=self.video_down_path)
            self.auto_utils.flag_one_video(bvid)


    def find_ups(self, ups=[]):
        for mid in tqdm(ups):
            self.findauthor(mid, down_pics=True, down_loc=self.user_dy_path, db_path=self.db_path)


class BlueSystem(object):
    __doc__ = """
    不获取视频和图片，专注于研究单个用户数据和用户关系
    """

    def __init__(self, db_path):
        self.db_path = db_path
        self.findauthor = run
        self.auto_utils = AutoUtils(db_path=self.db_path)

    def get_seed(self, ups=[]):
        for mid in tqdm(ups):
            self.findauthor(mid, down_pics=False, db_path=self.db_path, down_loc=None,
                            get_img=False, get_collect=False, get_update=True, vid_limit=20)

    def run(self):
        while True:
                mid = self.auto_utils.get_one_user()
            # try:
                self.findauthor(mid, down_pics=False, db_path=self.db_path, down_loc=None, get_img=False, get_collect=False, get_update=True, vid_limit=20)
            # except:
            #     self.auto_utils.flag_one_err_author(mid)


def main():
    argument = argparse.ArgumentParser()
    argument.add_argument('-s', '--seed-mid', default='``NULL``', type=str, help="Target user's mid (required).")
    argument.add_argument('-d', '--db', default='GREEN.DB', type=str, help='Database path.')
    argument.add_argument('-ud', '--user-dynamics', default='data/green/user_dynamics', type=str, help='User dynamic photos path.')
    argument.add_argument('-vp', '--video-path', default='data/green/videos', type=str, help='User Videos path.')
    argument.add_argument('-r', '--run', action='store_true', help='Enable Endless Running Mode. ')

    args = argument.parse_args()

    green_system = GreenSystem(db_path=args.db, user_dy_path=args.user_dynamics, video_down_path=args.video_path)
    if args.seed_mid != '```NULL```':
        green_system.find_ups([args.mid, ])
    if args.run:
        green_system.run()


def main_blue():
    blue_system = BlueSystem(db_path='BLUE.DB')
    # blue_system.get_seed(['13074237', ])
    blue_system.run()


if __name__ == '__main__':
    main_blue()