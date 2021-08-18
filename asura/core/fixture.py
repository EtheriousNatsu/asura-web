# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: fixture.py	
@time: 2021/8/17	
"""
from .builtin_assertion import VariableCaptureAssertion
from .exception import VariableCaptureError
from .generator import HttpReqGenerator, RandomGenerator
from .results import (HttpReqSetupResult, HttpReqTeardownResult,
                      RandomSetupResult)
from .selector import RandomDataSelector, get_http_selector


def get_step(step):
    """Return a Setup instance or Teardown instance.

        Args:
            step(:class:`steps.models.Step` instance): step instance

        Returns:
            :class:`core.fixture._Step` instance.

    """
    class_name = step.generator['type']
    return STEP_DICT[class_name](step)


class _Step:
    """Fixture base class.

    Args:
        step(:class:`steps.models.Step` instance): step instance

    Attributes:
        name(str): step name.
    """

    def __init__(self, step):
        self.name = step.name
        self.variables = step.variables
        self.generated_data = None
        self.result = None
        self.generator = None
        self.default_success_msg = 'Step %s completed' % self.name

    def run_capture_variable(self, namespace, variable):
        key = variable['name']
        value = self._run_capture_variable(namespace, variable)

        self._set_variable_into_namespace(namespace, key, value)
        self.result.add_log(key, value)

        return 'Captured variable %s' % key

    def _run_capture_variable(self, namespace, variable):
        raise NotImplementedError

    @staticmethod
    def _set_variable_into_namespace(namespace, key, value):
        """Store variable into namespace's dynamic_variables.

        Args:
            namespace(:obj:`core.namespace.Namespace`): variables db.
            key(str): variable key.
            value(str): variable value.
        """
        namespace.set_dynamic_variable(key, value)


class _Setup(_Step):
    """Setup Base class."""

    type = 'setup'

    def __init__(self, step):
        super().__init__(step)

    def run(self, namespace, result):
        self.generated_data = self.generator.generate(namespace, self.result)

        for variable in self.variables:
            variable_capture_assertion = VariableCaptureAssertion()
            variable_capture_assertion.run(self, namespace, variable, result)

    def _run_capture_variable(self, namespace, variable):
        raise NotImplementedError


class _Teardown(_Step):
    """Teardown Base class."""

    type = 'teardown'

    def __init__(self, step):
        super().__init__(step)

    def run(self, namespace, response, result):
        """"""
        self.generated_data = response

        for variable in self.variables:
            variable_capture_assertion = VariableCaptureAssertion()
            variable_capture_assertion.run(self, namespace, variable, result)

        return self.generator.generate(namespace, self.result)

    def _run_capture_variable(self, namespace, variable):
        raise NotImplementedError


class RandomSetup(_Setup):
    """Random setup.

    Args:
        step(:class:`steps.models.Step` instance): step instance

    Attributes:
        generator(:class:`core.generator._BaseGenerator` instance)
    """

    def __init__(self, step):
        super().__init__(step)
        self.generator = RandomGenerator(step.generator['settings'])
        self.result = RandomSetupResult(step.id)

    def run(self, namespace, result):
        """
        Use :class:`core.generator.RandomGenerator` instance
        to generate data.

        Args:
            namespace(:obj:`core.namespace.Namespace`): variables database.
            result(`instance of results.models.Result`)
        Returns:
            str
        """

        super().run(namespace, result)
        return self.default_success_msg

    def _run_capture_variable(self, namespace, variable):
        random_selector = RandomDataSelector(
            variable['type'],
            self.generated_data
        )
        return random_selector.parse()


class HttpReqSetup(_Setup):
    """Http request setup.

    Args:
        step(:class:`steps.models.Step` instance): step instance

    Attributes:
        generator(:class:`core.generator._BaseGenerator` instance)
    """

    def __init__(self, step):
        super().__init__(step)
        self.generator = HttpReqGenerator(step.generator['settings'])
        self.result = HttpReqSetupResult(step.id)

    def run(self, namespace, result):
        """
        Args:
            namespace(:obj:`core.namespace.Namespace`): variables database.
            result(`instance of results.models.Result`)
        Returns:
            str
        """
        super().run(namespace, result)
        status_code = self.generated_data.status_code
        msg = 'Step %s request completed (status %s)'
        return msg % (self.name, status_code)

    def _run_capture_variable(self, namespace, variable):
        http_selector = get_http_selector(
            variable['from'],
            variable['selector'],
            variable.get('selectorType', ''),
            self.generated_data
        )

        try:
            value = http_selector.parse()
        except VariableCaptureError:
            msg = 'Failed to capture variable %s in step %s using %s selector %s'
            msg = msg % (
                variable['name'],
                self.name,
                variable['selectorType'],
                variable['selector']
            )
            raise VariableCaptureError(msg)
        except Exception as e:
            msg = str(e)
            raise VariableCaptureError(msg)
        else:
            return value


class HttpReqTeardown(_Teardown):
    """Http request teardown.

    Args:
        step(:class:`steps.models.Step` instance): step instance

    Attributes:
        generator(:class:`core.generator._BaseGenerator` instance)
    """

    def __init__(self, step):
        super().__init__(step)
        self.generator = HttpReqGenerator(step.generator['settings'])
        self.result = HttpReqTeardownResult(step.id)

    def run(self, namespace, response, result):
        """

        1. get variables from test response.
        2. save it into dynamic_variables.
        3. call http.

        Args:
            namespace(:obj:`core.namespace.Namespace`): variables database.
            response(:obj:`requests.models.Response`): data source.
            result(`instance of results.models.Result`)

        """
        resp = super().run(namespace, response, result)

        status_code = resp.status_code
        msg = 'Step %s request completed (status %s)'
        return msg % (self.name, status_code)

    def _run_capture_variable(self, namespace, variable):
        """"""
        if self.generated_data is None:
            msg = 'Failed to capture variable %s in step %s' \
                '- test result dose not contain response'
            msg = msg % (variable['name'], self.name)
            raise VariableCaptureError(msg)

        http_selector = get_http_selector(
            variable['from'],
            variable['selector'],
            variable.get('selectorType', ''),
            self.generated_data
        )

        try:
            value = http_selector.parse()
        except VariableCaptureError:
            msg = 'Failed to capture variable %s in step %s using %s selector %s'
            msg = msg % (
                variable['name'],
                self.name,
                variable['selectorType'],
                variable['selector']
            )
            raise VariableCaptureError(msg)
        except Exception as e:
            msg = str(e)
            raise VariableCaptureError(msg)
        else:
            return value


STEP_DICT = {
    'RandomSetupGenerator': RandomSetup,
    'HttpReqSetupGenerator': HttpReqSetup,
    'HttpReqTeardownGenerator': HttpReqTeardown
}
