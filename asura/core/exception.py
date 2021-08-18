# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: exception.py	
@time: 2021/8/17	
"""


class BaseError(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg

    def __str__(self):
        return self.msg


class VariableCaptureError(BaseError):
    pass
