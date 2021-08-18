# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: urls.py	
@time: 2021/8/17	
"""
from django.urls import path

from .views import *


urlpatterns = [
    path('imports', ImportViewSet.as_view()),
]
