# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: builtin_assertion.py	
@time: 2021/8/17	
"""
from .exception import VariableCaptureError


class _BuiltAssertion:
    source = ''
    msg = ''

    def _serializer(self):
        return {
            'source': self.source,
            'msg': self.msg
        }


class SetupStepAssertion(_BuiltAssertion):
    """Built-in setup step assertion"""

    source = 'AssertSetupStep'

    def run(self, setup, namespace, result):
        try:
            self.msg = setup.run(namespace, result)
        except Exception as e:
            msg = 'Step %s failed - %s'
            self.msg = msg % (setup.name, str(e))

            result.assertions['failed'].insert(0, self._serializer())
            setup.result.add_log(log=self.msg)
        else:
            result.assertions['passed'].insert(0, self._serializer())
        finally:
            result.setups.append(setup.result.serializer())


class VariableCaptureAssertion(_BuiltAssertion):
    """Built-in capture variable assertion"""

    source = 'AssertVariableCapture'

    def run(self, step, namespace, variable, result):
        try:
            self.msg = step.run_capture_variable(namespace, variable)
        except VariableCaptureError as e:
            self.msg = str(e)
            result.assertions['failed'].insert(0, self._serializer())
        else:
            result.assertions['passed'].insert(0, self._serializer())


class TeardownStepAssertion(_BuiltAssertion):
    """Built-in teardown step assertion"""

    source = 'AssertTeardownStep'

    def run(self, teardown, namespace, response, result):
        try:
            self.msg = teardown.run(namespace, response, result)
        except Exception as e:
            msg = 'Step %s failed - %s'
            self.msg = msg % (teardown.name, str(e))

            teardown.result.add_log(self.msg)
            result.assertions['failed'].insert(0, self._serializer())
        else:
            result.assertions['passed'].insert(0, self._serializer())
        finally:
            result.teardowns.append(teardown.result.serializer())


class HttpRequestSuccessAssertion(_BuiltAssertion):
    """Built-in http request assertion"""

    source = 'AssertHttpRequestSuccess'

    def run(self, http_executor, result):
        try:
            resp = http_executor.run()
        except Exception as e:
            self.msg = str(e)
            result.assertions['failed'].insert(0, self._serializer())
        else:
            self.msg = 'Connected to host'
            result.assertions['passed'].insert(0, self._serializer())

            return resp
