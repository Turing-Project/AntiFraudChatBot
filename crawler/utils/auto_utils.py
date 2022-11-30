from utils.add_database import DBProxy

class AutoUtils:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db_proxy = DBProxy(db_path)
    def get_one_user(self):
        ret = self.db_proxy.select_one_author()
        return ret[0]

    def flag_one_video(self, bvid):
        self.db_proxy.flag_one_video(bvid)
        pass

    def get_one_vid(self,):
        return self.db_proxy.select_one_video()[0]

    def flag_one_err_author(self, mid):
        return self.db_proxy.flag_one_author_error(mid)


    def flag_one_user_done(self, mid):
        self.db_proxy.flag_one_author(mid)

if __name__ == '__main__':

    autoutils = AutoUtils('test2.db')
    # autoutils.get_one_user()
    print(autoutils.get_one_vid())
    # TODO:增加断点续传功能