# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: views.py	
@time: 2021/8/17	
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Environment
from .serializers import EnvironmentSerializer


class EnvironmentViewSet(ModelViewSet):
    """Environment CRUD"""

    serializer_class = EnvironmentSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Environment.objects.filter(
            service__user__id=self.request.user.pk
        )
