# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: models.py	
@time: 2021/8/17	
"""
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
from asura.services.models import Service
from asura.testcases.models import TestCase


class Hook(models.Model):
    action = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    vias = ArrayField(models.CharField(max_length=40))
    tests = models.ManyToManyField(TestCase)

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        db_table = 'hooks'

    def __str__(self):
        return '-'.join([self.type, self.action, self.target])
