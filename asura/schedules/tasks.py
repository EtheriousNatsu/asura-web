# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: tasks.py	
@time: 2021/8/18	
"""

import json
from datetime import datetime, timedelta

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.http import HttpRequest
from rest_framework.authtoken.models import Token
from rest_framework.request import Request

from asura.core.testsuite import RunnableTestSuite
from asura.users.models import User
from .models import Schedule
from .serializers import ScheduleSerializer


@shared_task()
def run_periodic_task(crontab_schedule_id, user_id):
    """Run periodic task.

        Args:
            crontab_schedule_id(int):
            user_id(int)
    """
    schedule = Schedule.objects.get(crontab_schedule=crontab_schedule_id)
    user = User.objects.get(pk=user_id)
    auth_token = Token.objects.get(user=user)
    tests = schedule.tests.all()

    if tests.exists():
        request = Request(HttpRequest())
        request.data['via'] = 'schedule'
        request.user = user
        request.auth = auth_token
        request.data['environment'] = schedule.environment.name
        runnable_suite = RunnableTestSuite(request, tests)
        runnable_suite.run()

        # set schedule lastRunId
        schedule.lastRunId = runnable_suite.result.name
    else:
        pass

    # set schedule nextRunTime
    schedule.nextRunTime = get_next_run_time(schedule.frequency)
    schedule.save()

    # serializer
    schedule_data = ScheduleSerializer(instance=schedule).data
    schedule_message = json.dumps(schedule_data)

    # socket
    group_name = 'asura_%s' % auth_token.key
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "process_schedule_message",
            'message': schedule_message
        }
    )


def get_next_run_time(frequency):
    """Get schedule next run time

        Args:
            frequency(str)
    """
    now = datetime.now()

    if frequency == 'SchedulePerOneMinutes':
        interval = timedelta(minutes=1)
    elif frequency == 'SchedulePerFiveMinutes':
        interval = timedelta(minutes=5)
    elif frequency == 'SchedulePerFifteenMinutes':
        interval = timedelta(minutes=15)
    elif frequency == 'SchedulePerThirtyMinutes':
        interval = timedelta(minutes=30)
    elif frequency == 'ScheduleHourly':
        interval = timedelta(minutes=60)
    elif frequency == 'ScheduleDaily':
        interval = timedelta(days=1)

    return now + interval

