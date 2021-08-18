# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: models.py
@time: 2021/8/16
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        verbose_name=_('email'),
        name='email',
        unique=True
    )

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.username
