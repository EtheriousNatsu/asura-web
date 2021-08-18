# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: utime.py	
@time: 2021/8/17	
"""
import random
import time
from datetime import datetime, timedelta


def generator_random_timestamp():
    """Generator a random timestamp

        Returns:
            str: a string representing the date in ISO format
    """
    start_datetime = 0
    end_datetime = int(time.time())
    timestamp = datetime(1970, 1, 1) + \
        timedelta(seconds=random.randint(start_datetime, end_datetime))

    return timestamp.isoformat()
