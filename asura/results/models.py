# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: models.py	
@time: 2021/8/17	
"""
import uuid

from django.contrib.postgres.fields import JSONField
from django.db import models

from asura.testcases.models import TestCase
from asura.testsuites.models import TestSuite


def get_assertions():
    return dict({'failed': [], 'passed': []})


class Result(models.Model):
    """Result model"""

    assertions = JSONField(
        default=get_assertions
    )
    setups = JSONField(
        default=list
    )
    teardowns = JSONField(
        default=list
    )
    requestScheme = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )
    requestBody = models.TextField(
        blank=True,
        null=True
    )
    requestHeaders = JSONField(
        default=list
    )
    requestHost = models.TextField(
        blank=True,
        null=True
    )
    requestMethod = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    requestPath = models.TextField(
        blank=True,
        null=True
    )
    requestQuery = models.TextField(
        blank=True,
        null=True
    )
    responseBody = models.TextField(
        blank=True,
        null=True
    )
    responseBodySize = models.IntegerField(
        blank=True,
        null=True
    )
    responseHeaders = JSONField(
        default=list
    )
    responseStatusCode = models.IntegerField(
        blank=True,
        null=True
    )
    responseTime = models.FloatField(
        blank=True,
        null=True
    )
    result = models.CharField(
        max_length=20,
        default='TestPending'
    )
    timestamp = models.DateTimeField(auto_now=True)

    test = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    testRun = models.ForeignKey(TestSuite, on_delete=models.CASCADE)

    def millisecond_response_time(self):
        """Return response time in milliseconds"""
        return int(self.responseTime * 1000)

    class Meta:
        db_table = 'results'
        ordering = ['-timestamp']
