# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: serializers.py	
@time: 2021/8/17	
"""
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Hook
from asura.testcases.serializers import TestCaseSerializer

MESSAGE = "A hook with this configuration already exists. Update the hook's settings and try again."


class HookSerializer(serializers.ModelSerializer):
    tests = TestCaseSerializer(many=True, read_only=True)

    class Meta:
        model = Hook
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Hook.objects.all(),
                fields=('action', 'target', 'vias', 'service'),
                message=MESSAGE
            )
        ]
