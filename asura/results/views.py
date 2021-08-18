# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: views.py	
@time: 2021/8/17	
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Result
from .serializers import ResultSerializer


class ResultViewSet(ModelViewSet):
    """Result view"""

    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Result.objects.filter(
            test__service__user__id=self.request.user.pk
        )
