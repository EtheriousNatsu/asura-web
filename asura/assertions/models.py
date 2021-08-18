# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: models.py	
@time: 2021/8/17	
"""
from django.db import models

from asura.testcases.models import TestCase


class Assertion(models.Model):

    comparator = models.CharField(max_length=120)
    property = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )
    source = models.CharField(max_length=120)
    target = models.CharField(max_length=120)

    test = models.ForeignKey(TestCase, on_delete=models.CASCADE)

    class Meta:
        db_table = 'assertions'
