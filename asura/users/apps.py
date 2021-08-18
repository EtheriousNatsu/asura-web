# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: apps.py	
@time: 2021/8/16
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'asura.users'
    verbose_name = '用户管理'

    def ready(self):
        import asura.users.signals
