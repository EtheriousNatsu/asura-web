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


class TestCase(models.Model):

    name = models.CharField(default='200 OK', max_length=120)
    description = models.CharField(
        blank=True,
        null=True,
        max_length=120
    )
    scheme = models.CharField(
        blank=True,
        null=True,
        max_length=120
    )
    endpoint = models.CharField(max_length=120)
    method = models.CharField(default='GET', max_length=120)
    headers = JSONField(
        default=list
    )
    params = JSONField(
        default=list
    )
    requestBody = JSONField(
        blank=True,
        null=True
    )
    variables = JSONField(
        default=list
    )

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    createdAt = models.DateTimeField(auto_now_add=True)

    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'testcases'

    def __str__(self):
        return self.name
