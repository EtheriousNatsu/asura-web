# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: serializers.py	
@time: 2021/8/17	
"""
import datetime

from rest_framework import serializers

from .models import Schedule
from asura.testcases.serializers import TestCaseSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    tests = TestCaseSerializer(many=True, read_only=True)
    startDate = serializers.DateTimeField(
        format="%Y/%m/%d %I:%M %p", input_formats=["%Y/%m/%d %I:%M %p"])

    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ('lastRunId', 'nextRunTime', 'crontab_schedule')
