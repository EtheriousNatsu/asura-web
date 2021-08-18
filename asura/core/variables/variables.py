# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: variables.py	
@time: 2021/8/17	
"""
from asura.core.utils import NormalizedDict

from .variablesplitter import VariableSplitter


class Variables(NormalizedDict):
    """Represents a set of variables.

    Contains methods for replacing variables from scalars, and strings.
    """

    def __init__(self):
        super().__init__(self, ignore=['_'])
        self._identifiers = ['$', ]

    def replace_scalar(self, item):
        """Replaces variables from a scalar item.

        If it is a ${scalar} variable its value is returned.
        Otherwise variables are replaced with 'replace_string'.
        """

        var = VariableSplitter(item, self._identifiers)
        if var.identifier and \
                var.base and var.start == 0 and var.end == len(item):
            return self._get_variable(var)
        return self._replace_string(item, var)

    def _replace_string(self, string, splitter=None):
        """Replaces variables from a string. Result is always a string.
        """
        result = []
        if splitter is None:
            splitter = VariableSplitter(string, self._identifiers)
        while True:
            if splitter.identifier is None:
                result.append(string)
                break
            result.append(string[:splitter.start])
            value = self._get_variable(splitter)
            result.append(value)
            string = string[splitter.end:]
            splitter = VariableSplitter(string, self._identifiers)
        result = ''.join(result)
        return result

    def _get_variable(self, var):
        """Return a ${scalar} variable's value.

        Args:
            var(VariableSplitter)
        """
        name = var.get_replaced_base()
        try:
            return self[name]
        except KeyError:
            return '%s{%s}' % (var.identifier, var.get_replaced_base())
