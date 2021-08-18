# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: text.py	
@time: 2021/8/17	
"""
import random
import string
import uuid


def generator_unique_str(prefix='', splitter='_', length=6):
    """Use uuid4 generator a unique string.

        Args:
            prefix (str): Prefix
            splitter (str): Splitter
            length (int): Unique string's length

        Returns:
            str: prefix + splitter + uuid.
    """
    return prefix + splitter + uuid.uuid4().hex[0:length]


def generator_random_str(size=6, chars=string.ascii_letters + string.digits):
    """Generator a random str

        Args:
            size(int): str length
            chars(str): data source

        Returns:
            str: random str.
    """
    return ''.join([random.choice(chars) for _ in range(size)])
