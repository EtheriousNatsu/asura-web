# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: assertion.py	
@time: 2021/8/17	
"""
import operator
import re

from .exception import VariableCaptureError
from .selector import get_http_selector


def get_assertion(assertion):
    """Return assertion instance

        Args:
            assertion(:obj:`assertions.models.Assertion`)
    """
    class_name = assertion.source
    return ASSERTION_DICT[class_name](assertion)


class _UserAssertion:
    """Base assertion class.

    Args:
        assertion(:obj:`assertions.models.Assertion`):

    Attributes:
        comparator(:obj:`function`): operator function.
        property(str): query string, like json path or xml path.
        source(str): assertion type.
        target(str): expected value.
        id(int):
        test(int):
    """

    def __init__(self, assertion):
        self.comparator = assertion.comparator
        self.property = assertion.property
        self.source = assertion.source
        self.target = assertion.target
        self.id = assertion.id
        self.test = assertion.test_id

    def run(self, namespace, response, result):
        raise NotImplementedError

    def _get_comparator_desc(self):
        str_list = re.findall('[A-Z][^A-Z]*', self.comparator)[1:]

        if 'Not' in str_list:
            str_list.remove('Not')
        else:
            str_list.insert(0, 'Not')

        return ' '.join(str_list).lower()

    def _serializer(self):
        return {
            'comparator': self.comparator,
            'property': self.property,
            'source': self.source,
            'target': self.target,
            'id': self.id,
            'test': self.test,
        }


class StatusCodeAssertion(_UserAssertion):
    """Assert http response status code.
    """

    def run(self, namespace, response, result):
        """

        1. get status code from `response`.
        2. use `namespace` to replace scalar `target`.
        3. use `comparator` to compare.

        Args:
            namespace(:obj:`core.namespace.Namespace`): variables database.
            response(:obj:`requests.models.Response`): data source.
            result(`instance of results.models.Result`)
        Returns:
            bool
        """
        status_code = response.status_code
        target = namespace.replace_scalar(self.target)
        comparator = OPERATOR_DICT[self.comparator]

        res = comparator(status_code, target)
        if res:
            result.assertions['passed'].insert(0, self._serializer())
        else:
            errors = []
            msg = 'Status code %s %s %s' % (
                status_code,
                self._get_comparator_desc(),
                target
            )
            errors.append(msg)

            local_dict = self._serializer()
            local_dict['errors'] = errors

            result.assertions['failed'].insert(0, local_dict)


class JsonPathAssertion(_UserAssertion):
    """Assert json response.
    """

    def run(self, namespace, response, result):
        """

        1. use `namespace` to replace scalar `target`.
        2. use `selector` to get actual value from json response.
        3. use `comparator` to compare.

        Args:
            namespace(:obj:`core.namespace.Namespace`): variables database.
            response(:obj:`requests.models.Response`): data source.
            result(`instance of results.models.Result`)

        Returns:
            bool
        """
        errors = []
        target = namespace.replace_scalar(self.target)
        comparator = OPERATOR_DICT[self.comparator]
        selector = namespace.replace_scalar(self.property)

        try:
            actual_value = get_http_selector(
                'body',
                selector,
                'JsonPathSelector',
                response
            ).parse()
        except VariableCaptureError:
            msg = 'Cannot select JSON value at path: %s' % selector
            errors.append(msg)
            local_dict = self._serializer()
            local_dict['errors'] = errors

            result.assertions['failed'].insert(0, local_dict)

        except Exception as e:
            msg = str(e)
            errors.append(msg)

            local_dict = self._serializer()
            local_dict['errors'] = errors

            result.assertions['failed'].insert(0, local_dict)
        else:
            res = comparator(actual_value, target)
            if res:
                result.assertions['passed'].insert(0, self._serializer())
            else:
                msg = 'JSON selection %s %s %s' % (
                    actual_value, self._get_comparator_desc(), target)

                errors.append(msg)

                local_dict = self._serializer()
                local_dict['errors'] = errors

                result.assertions['failed'].insert(0, local_dict)


class HeaderAssertion(_UserAssertion):
    """Assert http response headers.
    """

    def run(self, namespace, response, result):
        """

        1. use `namespace` to replace scalar `target`.
        2. use `selector` to get actual value from response headers.
        3. use `comparator` to compare.

        Args:
            namespace(:obj:`core.namespace.Namespace`): variables database.
            response(:obj:`requests.models.Response`): data source.
            result(`instance of results.models.Result`)

        Returns:
            bool
        """

        target = namespace.replace_scalar(self.target)
        comparator = OPERATOR_DICT[self.comparator]
        actual_value = get_http_selector(
            'header',
            namespace.replace_scalar(self.property),
            '',
            response
        ).parse()

        res = comparator(actual_value, target)

        if res:
            result.assertions['passed'].insert(0, self._serializer())
        else:
            errors = []
            msg = '%s header %s %s %s' % (
                self.property,
                actual_value,
                self._get_comparator_desc(),
                target
            )
            errors.append(msg)

            local_dict = self._serializer()
            local_dict['errors'] = errors

            result.assertions['failed'].insert(0, local_dict)


ASSERTION_DICT = {
    'AssertStatusCode': StatusCodeAssertion,
    'AssertJsonData': JsonPathAssertion,
    'AssertHeader': HeaderAssertion
}


OPERATOR_DICT = {
    'AssertEquals': lambda a, b: operator.eq(str(a), str(b)),
    'AssertNotEquals': lambda a, b: operator.ne(str(a), str(b)),
    'AssertLessThan': lambda a, b: operator.lt(float(a), float(b)),
    'AssertGreaterThan': lambda a, b: operator.gt(float(a), float(b)),
    'AssertContains': operator.contains,
    'AssertNotContains': lambda a, b: not operator.contains(a, b)
}
