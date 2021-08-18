# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: handlers.py	
@time: 2021/8/17	
"""
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.

    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        data = response.data
        response.data = {}
        message = ' '.join([''.join(message) for message in data.values()])
        response.data['code'] = 1
        response.data['msg'] = message
    return response
