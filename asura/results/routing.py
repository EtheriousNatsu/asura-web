# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: routing.py	
@time: 2021/8/18	
"""
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/asura/(?P<token>[^/]+)/$', consumers.ResultConsumer),
]
