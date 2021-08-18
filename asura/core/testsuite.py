# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: testsuite.py	
@time: 2021/8/17	
"""

import json
from urllib import parse

from asgiref.sync import async_to_sync
from celery import chord
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from .utils import generator_unique_str
from asura.environments.models import Environment
from asura.environments.serializers import EnvironmentSerializer
from asura.testcases.tasks import run_test
from asura.testsuites.models import TestSuite
from asura.testsuites.serializers import TestSuiteSerializer
from asura.testsuites.tasks import collect_tests_results


class RunnableTestSuite:
    """Runnable suite

    Args:
        request: django restful framework request
        tests(:class:`list` of `testcases.models.TestCase` instance):

    Attributes:
        result(:obj:`testsuites.models.TestSuite`):
        tests(:class:`list` of `testcases.models.TestCase` instance):
        trigger(str): trigger mode.
        group_name(str): channel group name.
        filter_by_endpoint(str): used to filter tests.
        filter_by_tests(:class:`list` of `int` instance): used to filter tests.
        environment(:obj:`environments.models Environment`): execution environment.
        via(str): trigger detail.

    """

    def __init__(self, request, tests):
        self.result = None
        self._parse_request_data(request, tests)
        self.tests = self._get_tests(tests)

    def run(self):
        """Use celery chods work-flow to run tests."""
        self._create_result()

        chord(
            run_test.s(
                self.group_name,
                self.result.pk,
                test.pk, self.environment.pk
            )
            for test in self.tests
        )(
            collect_tests_results.s(self.group_name, self.result.pk)
        )

    def _get_tests(self, tests):
        """
        filter tests by endpoint and primary key list, if filtered tests length
        equal 0, end request process immediately. otherwise return filtered tests.

        Args:
            tests(:class:`list` of `testcases.models.TestCase` instance):
        """
        q = tests

        if self.filter_by_endpoint:
            q = q.filter(endpoint=self.filter_by_endpoint)
        if self.filter_by_tests:
            q = q.filter(pk__in=self.filter_by_tests)

        if q.exists():
            return q
        else:
            data = {
                "code": "InvalidRequestError",
                "message": "At least one tests must be triggered."
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    def _create_result(self):
        """
        1. save `testsuites.models.TestSuite` into db.
        2. send message to front-end by websocket.
        """
        suite_name = self._get_suite_name()
        environment_data = EnvironmentSerializer(instance=self.environment).data

        self.result = TestSuite.objects.create(
            name=suite_name,
            executionEnvironment=environment_data,
            service=self.environment.service,
            via=self.via
        )

        self._send_suite_message()

    def _parse_request_data(self, request, tests):
        """parse request data"""
        self.environment = self._get_environment(request, tests)
        self.filter_by_endpoint = self._get_filter_by_endpoint(request)
        self.filter_by_tests = self._get_filter_by_tests(request)
        self.trigger = self._get_trigger(request)
        self.group_name = 'asura_%s' % request.auth.key
        self.via = {
            "account": request.user.pk,
            "type": 'Via' + self.trigger.capitalize(),
            "username": request.user.username
        }

    @staticmethod
    def _get_environment(request, tests):
        default_env = 'production'

        if request.query_params.get('environment'):
            current_env = request.query_params.get('environment')
        elif request.data.get('environment'):
            current_env = request.data.get('environment')
        else:
            current_env = default_env

        try:
            environment = get_object_or_404(
                Environment,
                name=current_env,
                service_id=tests[0].service.pk
            )
        except Environment.DoesNotExist:
            environment = get_object_or_404(
                Environment,
                name=default_env,
                service_id=tests[0].service.pk
            )

        return environment

    @staticmethod
    def _get_filter_by_endpoint(request):
        if request.query_params.get('endpoint'):
            return parse.unquote(request.query_params.get('endpoint'))
        elif request.data.get('endpoint'):
            return request.data.get('endpoint')
        else:
            return None

    @staticmethod
    def _get_filter_by_tests(request):
        default_tests = []

        try:
            if request.query_params.get('tests'):
                current_tests = list(map(int, request.query_params.get('tests').split(',')))
            elif request.data.get('tests'):
                current_tests = list(map(int, request.data.get('tests')))
            else:
                current_tests = default_tests
        except (TypeError, ValueError):
            return default_tests
        else:
            return current_tests

    @staticmethod
    def _get_trigger(request):
        default_trigger = 'url'
        trigger_list = ['dashboard', 'url', 'schedule']
        current_trigger = request.query_params.get('via')

        if current_trigger and current_trigger.lower() in trigger_list:
            return current_trigger
        else:
            current_trigger = request.data.get('via')
            if current_trigger and current_trigger.lower() in trigger_list:
                return current_trigger

        return default_trigger

    @staticmethod
    def _get_suite_name():
        """generate a unique suite name."""
        suite_name = generator_unique_str('test')

        while True:
            qs_exists = TestSuite.objects.filter(name=suite_name).exists()
            if not qs_exists:
                break
            else:
                suite_name = generator_unique_str('test')

        return suite_name

    def _send_suite_message(self):
        channel_layer = get_channel_layer()
        message = json.dumps(TestSuiteSerializer(instance=self.result).data)

        async_to_sync(channel_layer.group_send)(
            self.group_name,
            {
                "type": "process_suite_message",
                'message': message
            }
        )
