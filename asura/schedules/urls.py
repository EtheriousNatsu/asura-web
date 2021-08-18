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
    path('schedules/<int:schedule>/tests/<int:test>',ScheduleAndTestCaseView.as_view())
]
