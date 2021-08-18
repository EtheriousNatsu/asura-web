# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: models.py	
@time: 2021/8/17	
"""
from django.db import models
from asura.users.models import User


class Service(models.Model):

    name = models.CharField(max_length=120)
    schemes = models.CharField(max_length=120)
    host = models.CharField(max_length=120)
    icon = models.URLField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'services'

    def __str__(self):
        return self.name
