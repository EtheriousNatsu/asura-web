# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: tasks.py	
@time: 2021/8/17	
"""

import json

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from .models import TestCase
from asura.environments.models import Environment
from asura.results.serializers import ResultSerializer
from asura.testsuites.models import TestSuite

from asura.core.testcase import RunnableTestCase


@shared_task
def run_test(group_name, suite_id, test_id, env_id):
    """"Async execute test

        Args:
            group_name(str): channel group name.
            suite_id(int): Used to get `testsuites.models.TestSuite`.
            test_id(int): Used to get `testcases.models.TestCase`.
            env_id(int): Used to get `environments.models.Environment`
    """
    test = TestCase.objects.get(pk=test_id)
    env = Environment.objects.get(pk=env_id)
    suite = TestSuite.objects.get(pk=suite_id)

    # run and save
    runnable_test = RunnableTestCase(group_name, suite, test, env)
    result = runnable_test.async_run()
    result.save()

    # serializer
    case_data = ResultSerializer(instance=result).data
    case_message = json.dumps(case_data)

    # socket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "process_case_message",
            'message': case_message
        }
    )

    if result.result == 'TestPass':
        return True
    else:
        return False
