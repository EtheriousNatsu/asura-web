# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: serializers.py	
@time: 2021/8/17	
"""
from rest_framework import serializers

from .models import Result


class BaseResultSerializer(serializers.ModelSerializer):
    """Base result serializer"""
    executionEnvironment = serializers.SerializerMethodField(
        method_name='get_execution_environment',
        read_only=True
    )
    runId = serializers.SerializerMethodField(
        method_name='get_run_id',
        read_only=True
    )
    via = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = Result

    @staticmethod
    def get_execution_environment(obj):
        return obj.testRun.executionEnvironment

    @staticmethod
    def get_run_id(obj):
        return obj.testRun.name

    @staticmethod
    def get_via(obj):
        return obj.testRun.via


class ResultSerializer(BaseResultSerializer):
    """Result serializer"""
    class Meta(BaseResultSerializer.Meta):
        fields = '__all__'


class PartialResultSerializer(BaseResultSerializer):
    """Partial result

    Exclude `setups`, `teardowns`, `responseBody`
    """
    class Meta(BaseResultSerializer.Meta):
        exclude = ('setups', 'teardowns', 'responseBody')
