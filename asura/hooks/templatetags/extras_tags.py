# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: extras_tags.py	
@time: 2021/8/18	
"""
import os
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


ASSERTIONS_OPTIONS = {
    'AssertStatusCode': 'Status code',
    'AssertJsonData': 'JSON path data',
    'AssertVariableCapture': 'Variable capture',
    'AssertHttpRequestSuccess': 'HTTP request success',
    'AssertSetupStep': 'Setup step',
    'AssertTeardownStep': 'Teardown step'
}

COMPARISON_OPTIONS = {
    "AssertEquals": "Equal",
    "AssertNotEquals": "Does not equal",
    'AssertLessThan': 'Less than',
    'AssertGreaterThan': 'Greater than',
    'AssertContains': 'Contains',
    'AssertNotContains': 'Does not contain',
}


@register.filter
@stringfilter
def get_assertion_name(value):
    """
    According to assertion type, return name of the assertion.
    if not match, return None.

        Args:
            value: str

        Returns:
            str or None
    """
    return ASSERTIONS_OPTIONS.get(value)


@register.filter
@stringfilter
def get_assertion_comparison(value):
    """
    According to assertion comparison type, return name of the assertion
    comparison.if not macth, return None.

        Args:
            value: str
        Returns:
            str or None
    """
    return COMPARISON_OPTIONS.get(value)


@register.filter
def concat_strings(value, arg):
    """"""
    return str(value) + str(arg)


@register.filter
def get_result_assertions_desc(result, key):
    """Return result.assertion list

        Args:
            result: `results.models.Result`
            key: str

        Returns:
            str
    """
    failed_assertions_count = 0
    passed_assertions_count = 0

    if key == 'failed':
        failed_assertions_count = len(result.assertions.get(key))
        if failed_assertions_count > 1:
            return '{} assertions failed'.format(failed_assertions_count)
        return '{} assertion failed'.format(failed_assertions_count)
    else:
        passed_assertions_count = len(result.assertions.get(key))
        if passed_assertions_count > 1:
            return '{} assertions passed'.format(passed_assertions_count)
        return '{} assertion passed'.format(passed_assertions_count)


@register.filter
def get_test_link(result):
    """Return test link
        Args:
            result: `results.models.Result`

        Returns:
            str
    """
    return '{service_host}/dashboard/services/{service_id}/tests/{test_id}'.format(
        service_host=os.getenv('SERVICE_HOST'),
        service_id=result.testRun.service.id,
        test_id=result.test.id
    )
