# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: views.py	
@time: 2021/8/17	
"""
from rest_framework.viewsets import ModelViewSet

from .models import Assertion
from .serializers import AssertionSerializer


class AssertionsViewSet(ModelViewSet):

    serializer_class = AssertionSerializer
    queryset = Assertion.objects.all()
