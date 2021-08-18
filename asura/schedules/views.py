# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: views.py	
@time: 2021/8/17	
"""
import json

import dateutil.parser as parser
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Schedule
from .serializers import ScheduleSerializer
from asura.environments.models import Environment
from asura.services.models import Service
from asura.testcases.models import TestCase


class ScheduleViewSet(ModelViewSet):
    """Schedule view"""
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        """
        First create `django_celery_beat.models.CrontabSchedule`,
        then create `django_celery_beat.models.PeriodicTask`,
        final create `schedules.models.Schedule`
        """
        crontab = self.get_crontab(request.data['frequency'])
        start_date = self.get_start_date(request.data['startDate'])

        # create CrontabSchedule
        crontab_schedule = CrontabSchedule.objects.create(**crontab)
        # create PeriodicTask
        PeriodicTask.objects.create(
            crontab=crontab_schedule,
            name='periodic_task_%s' % crontab_schedule.pk,
            start_time=start_date,
            last_run_at=start_date,
            task='asura.schedules.tasks.run_periodic_task',
            args=json.dumps([crontab_schedule.pk, request.user.pk]),
        )

        service = Service.objects.get(pk=request.data['service'])
        env = Environment.objects.get(pk=request.data['environment'])
        schedule = Schedule.objects.create(
            frequency=request.data['frequency'],
            startDate=start_date,
            environment=env,
            service=service,
            crontab_schedule=crontab_schedule.pk
        )

        serializer1 = ScheduleSerializer(instance=schedule)
        return Response(serializer1.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        First update `django_celery_beat.models.PeriodicTask`,
        then update `django_celery_beat.models.CrontabSchedule`,
        final update `schedules.models.Schedule`
        """

        schedule = Schedule.objects.get(pk=kwargs['pk'])
        crontab_schedule = CrontabSchedule.objects.get(pk=schedule.crontab_schedule)
        # start_time = self.get_start_date(request.data['startDate'])

        # update PeriodicTask
        # for periodic_task in crontab_schedule.periodictask_set.all():
        #     # set utc timezone
        #     utc_start_time = start_time.astimezone(tz=utc)
        #     while utc_start_time != periodic_task.start_time:
        #         periodic_task.start_time = start_time
        #         periodic_task.last_run_at = start_time
        #         periodic_task.save()

        # update CrontabSchedule
        crontab = self.get_crontab(request.data['frequency'])
        for k, v in crontab.items():
            setattr(crontab_schedule, k, v)
        crontab_schedule.save()

        # update Schedule
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        return Schedule.objects.filter(
            service__user__id=self.request.user.pk
        )

    @staticmethod
    def get_start_date(start_date):
        """
        Convert datetime str to `datetime.datetime`
        instance, and timezone is `utc`

        Args:
            start_date(str)

        Returns:
            `datetime.datetime`
        """
        return parser.parse(start_date).replace(second=59, microsecond=999999)

    @staticmethod
    def get_crontab(frequency):
        """Construct a crontab dict

        Args:
            frequency(str)

        Returns:
            dict
        """
        crontab = {
            'minute': '*',
            'hour': '*',
            'day_of_week': '*',
            'day_of_month': '*',
            'month_of_year': '*',
        }
        if frequency == 'SchedulePerOneMinutes':
            crontab['minute'] = '*/1'
        elif frequency == 'SchedulePerFiveMinutes':
            crontab['minute'] = '*/5'
        elif frequency == 'SchedulePerFifteenMinutes':
            crontab['minute'] = '*/15'
        elif frequency == 'SchedulePerThirtyMinutes':
            crontab['minute'] = '*/30'
        elif frequency == 'ScheduleHourly':
            crontab['minute'] = '0'
            crontab['hour'] = '*/1'
        elif frequency == 'ScheduleDaily':
            crontab['minute'] = '0'
            crontab['hour'] = '0'

        return crontab


class ScheduleAndTestCaseView(APIView):
    """Association between test and schedule"""

    def post(self, request, *args, **kwargs):
        """Create association between test and schedule"""
        schedule_id = kwargs['schedule']
        test_id = kwargs['test']

        schedule = Schedule.objects.get(pk=schedule_id)
        test = TestCase.objects.get(pk=test_id)

        schedule.tests.add(test)
        serializer1 = ScheduleSerializer(instance=schedule)
        return Response(serializer1.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """Delete association between test and schedule"""
        schedule_id = kwargs['schedule']
        test_id = kwargs['test']

        schedule = Schedule.objects.get(pk=schedule_id)
        test = TestCase.objects.get(pk=test_id)

        schedule.tests.remove(test)
        return Response(status=status.HTTP_204_NO_CONTENT)
