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

from .models import TestSuite
from .serializers import TestSuiteSerializer
from asura.hooks.tasks import email_hook



@shared_task
def collect_tests_results(results, group_name, suite_id):
    """
    1. after all tests run, collect all tests results(true or false) to set suite result.
    2. send suite result to front-end by websocket.

        Args:
            group_name(str): channel group name.
            suite_id(int): Used to get `testsuites.models.TestSuite`.
            results(list): list of bool
    """
    if all(results):
        suite_status = 'TestRunPassed'
    else:
        suite_status = 'TestRunFailed'

    # save
    suite = TestSuite.objects.get(pk=suite_id)
    suite.status = suite_status
    suite.save()

    # serializer
    suite_data = TestSuiteSerializer(instance=suite).data
    suite_message = json.dumps(suite_data)

    # socket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "process_suite_message",
            'message': suite_message
        }
    )

    # send email
    email_hook.delay(suite_id)
