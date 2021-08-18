# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: unumber.py	
@time: 2021/8/17	
"""
import random


def generator_random_number(size=6):
    """Generator a random number

        Args:
                size(index optional): number length

        Returns:
                str: String form of random number.
    """
    return ''.join([str(random.randint(0, 9)) for _ in range(size)])
