# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: uuuid.py	
@time: 2021/8/17	
"""
import uuid


def generator_random_uuid():
    """Generator a random uuid

        Returns:
            str: a uuid string form.
    """
    return str(uuid.uuid4())
