# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: serializers.py	
@time: 2021/8/17	
"""
from rest_framework import serializers

from .models import (
    Setup,
    SetupAndTestCaseIntermediateTable,
    Teardown,
    TeardownAndTestCaseIntermediateTable
)
from asura.testcases.serializers import TestCaseSerializer


class StepSerializer(serializers.ModelSerializer):
    tests = TestCaseSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'


class SetupSerializer(StepSerializer):

    class Meta(StepSerializer.Meta):
        model = Setup


class TeardownSerializer(StepSerializer):

    class Meta(StepSerializer.Meta):
        model = Teardown


class SetupAndTestCaseIntermediateTableSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='setup_id')

    class Meta:
        model = SetupAndTestCaseIntermediateTable
        fields = ('step_number', 'id', )


class TeardownAndTestCaseIntermediateTableSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='teardown_id')

    class Meta:
        model = TeardownAndTestCaseIntermediateTable
        fields = ('step_number', 'id', )
