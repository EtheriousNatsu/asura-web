# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: models.py	
@time: 2021/8/17	
"""
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import F

from asura.services.models import Service
from asura.testcases.models import TestCase


class Step(models.Model):
    """Base class for setup and teardown"""

    name = models.CharField(max_length=128)
    generator = JSONField()
    variables = JSONField(default=list)

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Setup(Step):
    """Setup"""

    tests = models.ManyToManyField(
        TestCase, through='SetupAndTestCaseIntermediateTable')

    class Meta:
        db_table = 'setups'


class Teardown(Step):
    """Teardown"""

    tests = models.ManyToManyField(
        TestCase, through='TeardownAndTestCaseIntermediateTable')

    class Meta:
        db_table = 'teardowns'


class BaseIntermediateTable(models.Model):
    """Base intermediate table"""

    testcase = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = [F('step_number').asc(nulls_last=True)]


class SetupAndTestCaseIntermediateTable(BaseIntermediateTable):
    """"Setup and testcase intermediate table"""

    setup = models.ForeignKey(Setup, on_delete=models.CASCADE)

    class Meta(BaseIntermediateTable.Meta):
        db_table = 'setups_testcases'
        unique_together = (("testcase", "setup"),)


class TeardownAndTestCaseIntermediateTable(BaseIntermediateTable):
    """Teardown and testcase intermediate table"""

    teardown = models.ForeignKey(Teardown, on_delete=models.CASCADE)

    class Meta(BaseIntermediateTable.Meta):
        db_table = 'teardowns_testcases'
        unique_together = (("testcase", "teardown"),)
