# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: selector.py	
@time: 2021/8/17	
"""
from json.decoder import JSONDecodeError

from jsonpath_rw_ext import parser

from .exception import VariableCaptureError


class _BaseSelector:
    """Base selector class.

    Args:
        selector(str): Tool for selection.
        data(): data source.

    Attributes:
        selector(str): Tool for selection.
        data(): data source.
    """

    def __init__(self, selector, data):
        self.selector = selector
        self.data = data

    def parse(self):
        raise NotImplementedError


class RandomDataSelector(_BaseSelector):
    def parse(self):
        random_values = next(self.data)
        return random_values[self.selector]


def get_http_selector(where, selector, selector_type, data):
    """Base Selector class.

    According to `where` and `selector_type` to select
    selector.

    Args:
        where(str): e.g. body or header.
        selector(str): tool for selection.
        selector_type(str): selector type, you can pass `''`
        data(:obj:`requests.models.Response`): data source.

    Returns:
        :class:`core.selector._BaseSelector` instance
    """
    if where == 'header':
        return HeaderSelector(selector, data)
    else:
        return SELECTOR_DICT[selector_type](selector, data)


class JsonPathSelector(_BaseSelector):
    def parse(self):
        """Get values from JSON response body.

        Note: Only return the value found the first time.

        Returns:
            str
        """
        try:
            json_body = self.data.json()
            path_expr = parser.ExtentedJsonPathParser().parse(self.selector)
        except JSONDecodeError:
            msg = 'Failed to parse valid JSON from response body'
            raise Exception(msg)
        except Exception:
            msg = 'Json path syntax error'
            raise Exception(msg)
        else:
            matches = [match.value for match in path_expr.find(json_body)]
            if matches:
                return str(matches[0])
            else:
                raise VariableCaptureError('can not capture variable')


class HeaderSelector(_BaseSelector):
    def parse(self):
        """Get values from response headers.

        If selector in response headers, return it's value,
        return `''` otherwise.


        Returns:
            str
        """
        headers = self.data.headers

        return headers.get(self.selector, '')


SELECTOR_DICT = {
    'JsonPathSelector': JsonPathSelector,
    'HeaderSelector': HeaderSelector,
}
