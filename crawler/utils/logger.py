import time
import pandas as pd

def logger(info, type='INFO'):
    print('[{}]{}: {}'.format(time.strftime("%Y-%m-%d %H:%M:%S"),type, info))

def err_logger(err_msg, _id, err_code=0, err_log_path='err.log'):
    """
    0: following err
    1: danmaku err
    2: follower err
    3:

    :param err_msg:
    :param _id:
    :param status_code:
    :param err_log_path:
    :return:
    """
    df = pd.DataFrame([[err_msg, _id, err_code], ])
    df.to_csv(err_log_path, mode='a', header=None)


if __name__ == '__main__':
    pass
    # logger('qweqwe')
    # err_logger('123', '34')