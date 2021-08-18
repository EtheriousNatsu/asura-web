# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: urls.py	
@time: 2021/8/18	
"""
from django.urls import path
from .views import *

urlpatterns = [
    path('setups/<int:setup>/tests/<int:test>', SetupAndTestCaseView.as_view()),
    path('teardowns/<int:teardown>/tests/<int:test>', TeardownAndTestCaseView.as_view()),
]
