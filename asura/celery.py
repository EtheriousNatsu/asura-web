# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: celery.py	
@time: 2021/8/17	
"""
import os

from celery import Celery
import configurations
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asura.config')
os.environ.setdefault("DJANGO_CONFIGURATION", "Production")

configurations.setup()

app = Celery('asura')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
