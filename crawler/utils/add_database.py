from database.sql_executor import SQLHandler
from utils.logger import logger
import os
class DBProxy:
    def __init__(self, path):
        self.db_path = path
        if not os.path.exists(self.db_path):
            self.init_new_database()

    def create_table_follow(self):
        sql = """
        CREATE TABLE FOLL (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            MID INT NOT NULL,
            FOLLOWING INT NOT NULL,
            SPIDER_DONE INT DEFAULT 0,
            SPIDER_LOC INT DEFAULT 0
            );
        """
        sqlhandler = SQLHandler(self.db_path)
        sqlhandler.execute(sql)

    def create_table_ups(self):
        sql = """
        CREATE TABLE UPS (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            MID INT NOT NULL UNIQUE ,
            SPIDER_DONE INT DEFAULT 0,
            SPIDER_LOC INT DEFAULT 0
            );
        """
        sqlhandler = SQLHandler(self.db_path)
        sqlhandler.execute(sql)


    def insert_table_follow(self, mid, following, add_ups=True):
        sql = """
            INSERT INTO FOLL (MID, FOLLOWING) VALUES ("{}", "{}")
            """.format(
            mid, following
        )
        sqlhandler = SQLHandler(self.db_path)
        sqlhandler.execute(sql)
        if add_ups:
            sql = """
                        INSERT INTO UPS (MID) VALUES ("{}")
                        """.format(
                mid
            )
            sqlhandler = SQLHandler(self.db_path)
            sqlhandler.execute(sql)

    def see_table_follow(self):
        sql = """
                SELECT * FROM FOLL;
                """
        sqlhandler = SQLHandler(self.db_path)
        ret = sqlhandler.execute_return(sql)
        for i in ret:
            print(i)




    def create_table_collections(self, ):
        sql = """
            CREATE TABLE COLL (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            MID INT NOT NULL,
            VIDEOS TEXT,
            _COUNT_ INT,
            TITLE VARCHAR(255),
            _TIME INT
            );
            """
        sqlhandler = SQLHandler(self.db_path)
        sqlhandler.execute(sql)

    def insert_table_collections(self, info_d):
        sql = """
        INSERT INTO COLL (MID, VIDEOS, _COUNT_, TITLE) VALUES ("{}", "{}", "{}", "{}")
        """.format(
            info_d['mid'],
            info_d['videos'],
            info_d['count'],
            info_d['title']
        )
        sqlhandler = SQLHandler(self.db_path)
        sqlhandler.execute(sql)

    def see_table_collections(self):
        sql = """
            SELECT * FROM COLL;
            """
        sqlhandler = SQLHandler(self.db_path)
        ret = sqlhandler.execute_return(sql)
        for i in ret:
            print(i)

    def create_table_dynamics(self):
        sql = """
        CREATE TABLE DYNA (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        MID INT NOT NULL,
        _FROM INT,
        ORIGIN_SAY TEXT,
        SAY TEXT,
        PICS TEXT,
        REPLY INT,
        _TIME INT,
        LIKE INT,
        SHARE INT
        );
        """
        sqlhandler = SQLHandler(self.db_path)
        sqlhandler.execute(sql)

    def insert_table_dynamics(self, info_d, mid):
        sql = """
        INSERT INTO DYNA (MID, _FROM, ORIGIN_SAY, SAY, PICS, REPLY, _TIME) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}")
        """.format(mid,
                   info_d['from'],
                   info_d['origin_say'],
                   info_d['say'],
                   info_d['pics'],
                   info_d['reply'],
                   info_d['upload_time']
                   )
        # print(sql)
        sqlhandler = SQLHandler(self.db_path)
        sqlhandler.execute(sql)

    def create_table_author(self):
        pass
        sql = """
        CREATE TABLE AUTHOR(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        FOLLOWER INT,
        FOLLOWING INT,
        MID INT NOT NULL UNIQUE ,
        KEYWORDS VARCHAR(255),
        NAME VARCHAR(255),
        SEX VARCHAR(50),
        FACE_URL VARCHAR(255),
        SIGN TEXT,
        RANK INT,
        LEVEL INT,
        JOINTIME INT,
        BIRTHDAY INT,
        OFFICIAL VARCHAR(255),
        VIP_TYPE INT,
        VIP_STATUS INT,
        VIP_DUE INT,
        VIP_PAY_TYPE INT,
        LIVE_INFO VARCHAR(255),
        LIVE_TITLE VARCHAR(255),
        LIVE_COVER VARCHAR(255),
        SPIDER_TIME FLOAT,
        APPENDIX_1 INT,
        APPENDIX_2 VARCHAR(255),
        APPENDIX_3 TEXT,
        FACE_IMG BLOB,
        LIVE_COVER_IMG BLOB
        );
        """
        sqlhandler = SQLHandler(self.db_path)
        sqlhandler.execute(sql)

    def see_table_author(self):
        sql = """
        SELECT COUNT(*) FROM AUTHOR;
        """
        sqlhandler = SQLHandler(self.db_path)
        ret = sqlhandler.execute_return(sql)
        for i in ret:
            print(i)

    def see_table_dynamics(self):
        sql = """
        SELECT * FROM DYNA;
        """
        sqlhandler = SQLHandler(self.db_path)
        ret = sqlhandler.execute_return(sql)
        for i in ret:
            print(i)

    def insert_table_author(self, info_d):
        sql = """
        INSERT INTO AUTHOR (FOLLOWER, FOLLOWING, MID, KEYWORDS, NAME, SEX, FACE_URL, SIGN, RANK, LEVEL, JOINTIME, BIRTHDAY, OFFICIAL, VIP_TYPE, VIP_STATUS, VIP_DUE, VIP_PAY_TYPE, LIVE_INFO, LIVE_TITLE, LIVE_COVER, SPIDER_TIME) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")""".format(
            info_d['follower'],
            info_d['following'],
            info_d['mid'],
            info_d['key_words'],
            info_d['name'],
            info_d['sex'],
            info_d['face'],
            info_d['sign'],
            info_d['rank'],
            info_d['level'],
            info_d['jointime'],
            info_d['birthday'],
            info_d['official'],
            info_d['vip_type'],
            info_d['vip_status'],
            info_d['vip_due'],
            info_d['vip_pay_type'],
            info_d['live_info'],
            info_d['live_title'],
            info_d['live_cover'],
            info_d['spider_time'],
            # info_d['face_img'],
            # info_d['cover_img']
        )
        # print(sql)
        # quit()
        sqlhandler = SQLHandler(self.db_path)
        sqlhandler.execute(sql)

        # FACE_IMG, LIVE_COVER_IMG
        sql_2 = """UPDATE AUTHOR SET FACE_IMG=? WHERE MID={}""".format(info_d['mid'])
        sqlhandler.insert_binary(sql_2, bin_obj=info_d['face_img'])
        sql_3 = """UPDATE AUTHOR SET LIVE_COVER_IMG=? WHERE MID={}""".format(info_d['mid'])
        sqlhandler.insert_binary(sql_3, bin_obj=info_d['cover_img'])







    def create_table_video(self):
        sql = """
                CREATE TABLE VID (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                MID INT NOT NULL,
                BVID VARCHAR(20) UNIQUE NOT NULL,
                TITLE VARCHAR(255),
                DESCRIPTION TEXT,
                M_DM TEXT,
                _TIMESTAMP_ INT,
                _LIKE_ INT,
                COMMENT_COUNT INT,
                COVER_URL VARCHAR(255),
                PLAY_COUNT INT,
                VID_LENGTH VARCHAR(20),
                COVER_IMG BLOB,
                DOWNLOADED INT DEFAULT 0,
                DOWN_LOC INT DEFAULT 0,
                APPENDIX_1 INT,
                APPENDIX_2 VARCHAR(255),
                APPENDIX_3 TEXT
                );
                """
        sqlhandler = SQLHandler(self.db_path)
        sqlhandler.execute(sql)

    def insert_table_video(self, info_d):
        sql = """
        INSERT INTO VID (MID, BVID, TITLE, DESCRIPTION, M_DM, _TIMESTAMP_, COMMENT_COUNT, COVER_URL, PLAY_COUNT, VID_LENGTH) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");
        """.format(
            info_d['mid'],
            info_d['bvid'],
            info_d['title'],
            info_d['description'],
            info_d['dm'],
            info_d['created'],
            info_d['comment'],
            info_d['pic'],
            info_d['play'],
            info_d['length']
        )
        # print(sql)
        sqlhandler = SQLHandler(self.db_path)
        sqlhandler.execute(sql)
        sql_2 = """
        UPDATE VID SET COVER_IMG=? WHERE MID={}
        """.format(info_d['mid'])
        sqlhandler.insert_binary(sql_2, info_d['cover'])

    def see_table_video(self):
        sql = """
            SELECT MID, BVID, TITLE, DESCRIPTION, M_DM, PLAY_COUNT, VID_LENGTH FROM VID;
            """
        sqlhandler = SQLHandler(self.db_path)
        ret = sqlhandler.execute_return(sql)
        for i in ret:
            print(i)

    def see_table_ups(self):
        sql = """
            SELECT ID, SPIDER_DONE FROM UPS;
            """
        sqlhandler = SQLHandler(self.db_path)
        ret = sqlhandler.execute_return(sql)
        for i in ret:
            print(i)

    def select_one_author(self):
        sql = """
        SELECT MID FROM UPS WHERE SPIDER_DONE=0 ORDER BY ID ASC LIMIT 1;
        """
        sqlhandler = SQLHandler(self.db_path)
        ret = sqlhandler.execute_return(sql)
        logger('New author selected.')
        for i in ret:
            return i

    def flag_one_author(self, mid):
        sql = """
        UPDATE UPS SET SPIDER_DONE=1 WHERE MID="{}";
        """.format(mid)
        sqlhandler = SQLHandler(self.db_path)
        sqlhandler.execute(sql)

    def select_one_video(self):
        sql = """
        SELECT BVID FROM VID WHERE DOWNLOADED=0 ORDER BY ID ASC LIMIT 1;
        """
        sqlhandler = SQLHandler(self.db_path)
        ret = sqlhandler.execute_return(sql)
        logger('New video selected.')
        for i in ret:
            return i

    def flag_one_video(self, bvid):
        sql = """
          UPDATE VID SET DOWNLOADED=1 WHERE BVID="{}";
        """.format(bvid)
        # print(sql)
        sqlhandler = SQLHandler(self.db_path)
        sqlhandler.execute(sql)

    def flag_one_author_error(self, mid):
        sql = """
        UPDATE UPS SET SPIDER_DONE = 3 WHERE MID = "{}"
        """.format(mid)
        sqlhandler = SQLHandler(self.db_path)
        sqlhandler.execute(sql)


    def db_handler(self):
        sql = """
        UPDATE UPS SET SPIDER_DONE = 0 WHERE ID >868;
        """
        sqlhandler = SQLHandler(self.db_path)
        sqlhandler.execute(sql)




    def init_new_database(self):
        logger('Initing new databases...')
        self.create_table_video()
        logger('Video table created.')
        self.create_table_follow()
        logger('Follow table created.')
        self.create_table_collections()
        logger('Collection table created.')
        self.create_table_dynamics()
        logger('Dynamics table created.')
        self.create_table_author()
        logger('Author table created.')
        self.create_table_ups()
        logger('UPS table created.')

# def create_table_relation():




if __name__ == '__main__':
    # create_table_author()
    # see_table_author()
    # create_table_dynamics()
    # see_table_dynamics()
    # create_table_collections()
    # see_table_collections()
    # create_table_follow()
    # see_table_follow()
    # create_table_video()
    # see_table_video()
    dbproxy = DBProxy('../BLUE.DB')
    # dbproxy.see_table_author()
    # dbproxy.see_table_follow()
    # dbproxy.see_table_dynamics()
    # dbproxy.select_one_author()
    # dbproxy.see_table_video()
    # dbproxy.create_table_ups()
    dbproxy.see_table_ups()
    # dbproxy.db_handler()
    # dbproxy.see_table_dynamics()
    # TODO:目前动态只能下载其中的一张照片，需要修复,但是获取的过程是没有问题的，动态无法获取完全
    pass