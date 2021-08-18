# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: serializers.py	
@time: 2021/8/17	
"""
from rest_framework import serializers

from .models import TestSuite


class TestSuiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestSuite
        fields = '__all__'
