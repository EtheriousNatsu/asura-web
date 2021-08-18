# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: models.py	
@time: 2021/8/17	
"""
from django.db import models

from asura.environments.models import Environment
from asura.services.models import Service
from asura.testcases.models import TestCase

# Create your models here.


class Schedule(models.Model):

    frequency = models.CharField(max_length=200)
    startDate = models.DateTimeField()
    lastRunId = models.CharField(max_length=100, blank=True, null=True)
    nextRunTime = models.DateTimeField(blank=True, null=True)

    environment = models.ForeignKey(
        Environment, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    tests = models.ManyToManyField(TestCase)

    crontab_schedule = models.IntegerField()

    class Meta:
        db_table = 'schedules'

    def __str__(self):
        return self.frequency
