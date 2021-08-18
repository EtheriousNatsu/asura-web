# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: views.py	
@time: 2021/8/17	
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import TestSuite
from .serializers import TestSuiteSerializer


class TestSuiteViewSet(ModelViewSet):

    serializer_class = TestSuiteSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return TestSuite.objects.filter(
            service__user__id=self.request.user.pk
        )
