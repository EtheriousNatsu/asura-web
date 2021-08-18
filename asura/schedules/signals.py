# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: signals.py	
@time: 2021/8/17	
"""
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django_celery_beat.models import CrontabSchedule

from .models import Schedule


@receiver(post_delete, sender=Schedule,
          dispatch_uid="delete_crontab_schedule")
def delete_crontab_schedule(sender, instance, **kwargs):
    """Delete `django_celery_beat.models.CrontabSchedule` instance"""
    if instance:
        cron_schedule_id = instance.crontab_schedule
        crontab_schedule = CrontabSchedule.objects.get(pk=cron_schedule_id)
        crontab_schedule.delete()
