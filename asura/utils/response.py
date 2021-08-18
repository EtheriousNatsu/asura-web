# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: response.py	
@time: 2021/8/17	
"""
from rest_framework.response import Response


class ResponseOk(Response):
    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        response_data = {
            'code': 0,
            'msg': 'success',
            'data': data,
        }
        super().__init__(response_data, status,
                         template_name, headers,
                         exception, content_type)
