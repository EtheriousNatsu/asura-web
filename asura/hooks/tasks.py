# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: tasks.py	
@time: 2021/8/17	
"""
import re
import os

from celery import shared_task
from django.db.models import Q

from .models import Hook
from asura.tasks import send_email
from asura.testsuites.models import TestSuite

HTML_EMAIL_TEMPLATE_NAME = 'email/tests_report.html'
EMAIL_TEMPLATE_NAME = 'email/tests_report.txt'


@shared_task
def email_hook(suite_id):
    """email hook


        Args:
            suite_id(int): Used to get `testsuites.models.TestSuite`.
    """
    print(suite_id)
    suite = TestSuite.objects.get(pk=suite_id)
    # filter hook by service id and trigger type
    hooks = Hook.objects.filter(Q(service=suite.service) & Q(vias__contains=[suite.via['type']]))

    if hooks.exists():
        all_tests_results = suite.result_set
        for hook in iter(hooks):
            if hook.tests.exists():
                hook_tests_results = all_tests_results.filter(test__in=hook.tests.all())
                if hook_tests_results.exists():
                    if hook.action == 'OnTestFailure':
                        hook_tests_results = hook_tests_results.filter(result='TestFail')
                    if hook_tests_results.exists():
                        context = build_context(suite, hook_tests_results)
                        send_email(
                            subject_template_name=EMAIL_TEMPLATE_NAME,
                            email_template_name=None,
                            context=context,
                            from_email=os.getenv('EMAIL_HOST_USER'),
                            to_email=[hook.target, ],
                            html_email_template_name=HTML_EMAIL_TEMPLATE_NAME
                        )


def build_context(suite, hook_tests_results):
    """Build a context for render template.

        Args:
            suite(:class: `testsuites.models.TestSuite` instance)
            hook_tests_results(:class: `django.db.models.query.QuerySet` instance)

        Returns:
            context(dict)
    """
    base_link = '{service_host}/dashboard/services/{service_id}'.format(
        service_host=os.getenv('SERVICE_HOST'),
        service_id=suite.service.id
    )
    context = {
        'suite': suite,
        'tests_results': hook_tests_results,
        'tests_count_description': build_tests_count_description(hook_tests_results),
        'tests_assertions_description': build_tests_assertions_description(hook_tests_results),
        'run_link': build_run_link(base_link, suite),
        'run_id': build_run_id(suite),
        'setting_link': build_setting_link(base_link),
        'execution_environment_name': build_execution_environment_name(suite),
        'results_link': build_results_link(base_link),
        'trigger_mode': build_trigger_mode(suite),
        'service_icon_link': build_service_icon_link(suite),
        'service_link': build_service_link(suite),
        'execution_environment_link': build_execution_environment_link(suite),
        'tests_status_description': build_tests_status_description(hook_tests_results),
        'triggerBy': suite.via['username'],
        'subject_tests_status_description': build_subject_tests_status_description(suite, hook_tests_results)
    }

    return context


def build_tests_count_description(hook_tests_results):
    """Build tests_count_description

        Args:
            hook_tests_results(:class: of `django.db.models.query.QuerySet` instance)

        Returns:
            str
    """
    tests_count = hook_tests_results.count()
    tests_count_description = '{} test'.format(tests_count)
    if tests_count > 1:
        tests_count_description += 's'

    return tests_count_description


def build_tests_assertions_description(hook_tests_results):
    """Build hook_tests_results

        Args:
            hook_tests_results(:class: of `django.db.models.query.QuerySet` instance)

        Returns:
            str
    """
    tests_assertions_count = 0
    for result in iter(hook_tests_results):
        tests_assertions_count += len(result.assertions['failed'])
        tests_assertions_count += len(result.assertions['passed'])

    return '{} assertions'.format(tests_assertions_count)


def build_run_id(suite):
    """Build run_id

        Args:
            suite(:class: `testsuites.models.TestSuite` instance)

        Returns:
            str
    """
    return suite.name


def build_run_link(base_link, suite):
    """Build run_link

        Args:
            base_link(str)
            suite(:class: `testsuites.models.TestSuite` instance)

        Returns:
            str
    """
    run_link = base_link + '/results/{}'
    return run_link.format(suite.name)


def build_execution_environment_name(suite):
    """Build execution_environment_name

        Args:
            suite(:class: `testsuites.models.TestSuite` instance)

        Returns:
            str
    """
    return suite.executionEnvironment['name']


def build_setting_link(base_link):
    """Build setting_link

        Args:
            base_link(str)

        Returns:
            str
    """
    setting_link = base_link + '/settings'
    return setting_link


def build_trigger_mode(suite):
    """Build trigger_mode

        Args:
            suite(:class: `testsuites.models.TestSuite` instance)

        Returns:
            str
    """
    return ' '.join(re.findall('[A-Z][^A-Z]*', suite.via['type'])).lower()


def build_results_link(base_link):
    """Build results_link

        Args:
            base_link(str)

        Returns:
            str
    """
    return base_link + '/results'


def build_service_icon_link(suite):
    """Build service_icon_link

        Args:
            suite(:class: `testsuites.models.TestSuite` instance)

        Returns:
            str
    """
    return suite.service.icon


def build_service_link(suite):
    """Build service_link

        Args:
            suite(:class: `testsuites.models.TestSuite` instance)

        Returns:
            tuple
    """
    return 'http://' + suite.service.host, suite.service.host


def build_execution_environment_link(suite):
    """Build execution_environment_link

        Args:
            suite(:class: `testsuites.models.TestSuite` instance)

        Returns:
            tuple
    """
    return 'http://' + suite.executionEnvironment['url'], suite.executionEnvironment['url']


def build_tests_status_description(hook_tests_results):
    """Build failed_tests_description

        Args:
            hook_tests_results(:class: of `django.db.models.query.QuerySet` instance)

        Returns:
            tuple
    """
    failed_tests_count = 0
    passed_tests_count = 0
    failed_tests_description = ''
    passed_tests_description = ''

    for result in iter(hook_tests_results):
        if result.result == 'TestFail':
            failed_tests_count += 1
        elif result.result == 'TestPass':
            passed_tests_count += 1

    if failed_tests_count > 1:
        failed_tests_description = '{} tests failed'.format(failed_tests_count)
    else:
        failed_tests_description = '{} test failed'.format(failed_tests_count)

    if passed_tests_count > 1:
        passed_tests_description = '{} tests passed'.format(passed_tests_count)
    else:
        passed_tests_description = '{} test passed'.format(passed_tests_count)

    return failed_tests_description, passed_tests_description


def build_subject_tests_status_description(suite, hook_tests_results):
    """Build subject_tests_status_description

        Args:
            suite(:class: `testsuites.models.TestSuite` instance)
            hook_tests_results(:class: `django.db.models.query.QuerySet` instance)


        Returns:
            str
    """
    if suite.status == 'TestRunPassed':
        return '{} tests passed'.format(hook_tests_results.count())
    else:
        failed_tests_count = 0
        for result in iter(hook_tests_results):
            if result.result == 'TestFail':
                failed_tests_count += 1
        return '{}/{} tests failed'.format(failed_tests_count, hook_tests_results.count())
