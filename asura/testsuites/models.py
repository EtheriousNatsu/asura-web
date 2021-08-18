# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: models.py	
@time: 2021/8/17	
"""
from django.contrib.postgres.fields import JSONField
from django.db import models

from asura.services.models import Service


class TestSuite(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    executionEnvironment = JSONField()
    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20,
        default="TestRunPending"
    )
    updatedAt = models.DateTimeField(auto_now=True)
    via = JSONField()

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        db_table = 'testsuites'

    def __str__(self):
        return self.name
