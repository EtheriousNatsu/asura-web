# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: testcase.py	
@time: 2021/8/17	
"""

import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .assertion import get_assertion
from .builtin_assertion import (
    HttpRequestSuccessAssertion,
    SetupStepAssertion,
    TeardownStepAssertion
)
from .fixture import get_step
from .http import HttpExecutor
from .namespace import Namespace

from asura.results.models import Result
from asura.results.serializers import ResultSerializer
from asura.steps.models import Setup, Teardown
from asura.assertions.models import Assertion


class RunnableTestCase:
    """Runnable test

    Args:
        group_name(str): channel group name.
        suite(:obj:`results.models.Result`): this test belong this suite.
        test(:obj:`testcases.models.TestCase`):
        env(:obj:`environments.models.Environment`): execution environment.

    Attributes:
        result(:obj:`results.models.Result`)
        group_name(str): channel group name.
        suite(:obj:`results.models.Result`): this test belong this suite.
        test(:obj:`testcases.models.TestCase`):
        name(str): test name.
        description(str): test description.
        scheme(str):
        host(str):
        path(str):
        method(str):
        headers(list):
        params(list):
        body(dict)
        variables(:obj:`list` of :obj:`dict`): test local variables.
        setups(:obj:`list` of :class:`core.fixture._step` instance): setups.
        teardowns(:obj:`list` of :class:`core.fixture._step` instance):
        assertions(:class:`list` of `core.assertion._UserAssertion` instance)
        service(:obj:`services.models.Service`):
        env(:obj:`environments.models.Environment`): execution environment.
    """

    def __init__(self, group_name, suite, test, env):
        self.result = None
        self.test = test
        self.suite = suite
        self.group_name = group_name

        self.service = env.service
        self.env = env
        self._init_test(test)
        self._init_setups(test)
        self._init_teardowns(test)
        self._init_assertions(test)

    def _init_test(self, test):
        self.name = test.name
        self.description = test.description
        self.scheme = test.scheme
        self.host = self.env.url
        self.path = test.endpoint
        self.method = test.method
        self.headers = test.headers
        self.params = test.params
        self.body = test.requestBody
        self.variables = test.variables

    def _init_setups(self, test):
        self.setups = []
        for setup in self._get_setups(test):
            self.setups.append(get_step(setup))

    def _init_teardowns(self, test):
        self.teardowns = []
        for teardown in self._get_teardowns(test):
            self.teardowns.append(get_step(teardown))

    def _init_assertions(self, test):
        self.assertions = []
        for assertion in self._get_assertions(test):
            self.assertions.append(get_assertion(assertion))

    def async_run(self):
        """Async execute test"""
        self._start_run()
        self._run_setups(self.result)
        response = self._run_test(self.result)
        self._run_teardowns(response, self.result)
        self._run_assertions(response, self.result)

        self._set_case_status(self.result)

        return self.result

    @staticmethod
    def _set_case_status(result):
        """
        According to result's assertions to set case status.
        """
        if len(result.assertions['failed']) > 0:
            result.result = 'TestFail'
        else:
            result.result = 'TestPass'

    def _start_run(self):
        """Preparation before performing the test.

        1. create result
        2. create execution context.
        """
        self._create_result()
        self._create_namespace()

    def _create_result(self):
        """
        1. save `results.models.Result` into db.
        2. send message to front-end by websocket.
        """
        self.result = Result.objects.create(
            test=self.test,
            testRun=self.suite
        )

        self._send_case_message()

    def _send_case_message(self):
        channel_layer = get_channel_layer()
        message = json.dumps(ResultSerializer(instance=self.result).data)

        async_to_sync(channel_layer.group_send)(
            self.group_name,
            {
                "type": "process_case_message",
                'message': message
            }
        )

    def _create_namespace(self):
        """Create a test execution context.

        First deepcopy suite's namespace, then
        set test variables into namespace.
        """
        self.namespace = Namespace()

        self.namespace.set_global_variable(
            'service_scheme', self.service.schemes)
        self.namespace.set_global_variable('service_host', self.service.host)
        self.namespace.set_global_variable(
            'execution_environment_host', self.env.url)

        for variable in self.env.variables:
            self.namespace.set_environment_variable(**variable)

        for variable in self.variables:
            self.namespace.set_test_variable(**variable)

    def _run_test(self, result):
        http_executor = HttpExecutor(
            self.scheme,
            self.host,
            self.path,
            self.method,
            self.namespace,
            result,
            headers=self.headers,
            params=self.params,
            body=self.body
        )
        http_req_assertion = HttpRequestSuccessAssertion()
        resp = http_req_assertion.run(http_executor, result)

        return resp

    def _run_setups(self, result):
        for setup in self.setups:
            setup_assertion = SetupStepAssertion()
            setup_assertion.run(setup, self.namespace, result)

    def _run_teardowns(self, response, result):
        for teardown in self.teardowns:
            teardown_assertion = TeardownStepAssertion()
            teardown_assertion.run(teardown, self.namespace, response, result)

    def _run_assertions(self, response, result):
        if response is None:
            return

        for assertion in self.assertions:
            assertion.run(self.namespace, response, result)

    @staticmethod
    def _get_setups(test):
        """Query `database`, return :obj:`setups.models.Setup`"""
        return Setup.objects.filter(tests__id=test.id).order_by('setupandtestcaseintermediatetable__step_number')

    @staticmethod
    def _get_teardowns(test):
        """Query `database`, return :obj:`teardowns.models.Teardown`"""
        return Teardown.objects.filter(tests__id=test.id).order_by('teardownandtestcaseintermediatetable__step_number')

    @staticmethod
    def _get_assertions(test):
        """Query `database`, return :obj:`assertions.models.Assertion`"""
        return Assertion.objects.filter(test_id=test.id)
