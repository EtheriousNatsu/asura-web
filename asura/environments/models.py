# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: models.py	
@time: 2021/8/17	
"""
from django.contrib.postgres.fields import JSONField
from django.db import models

from asura.services.models import Service


# Create your models here.
class Environment(models.Model):
    """Environment"""

    name = models.CharField(max_length=120)
    url = models.CharField(max_length=120)
    variables = JSONField(
        default=list
    )

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        db_table = 'environments'
        ordering = ["id"]
        unique_together = ('name', 'service')

    def __str__(self):
        return self.name
