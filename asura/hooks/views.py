# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: views.py	
@time: 2021/8/17	
"""
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Hook
from .serializers import HookSerializer
from asura.testcases.models import TestCase


class HookViewSet(ModelViewSet):

    serializer_class = HookSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Hook.objects.filter(
            service__user__id=self.request.user.pk
        )


class HookAndTestCaseView(APIView):

    def post(self, request, *args, **kwargs):
        """Create association between test and hook"""
        hook_id = kwargs['hook']
        test_id = kwargs['test']

        hook = Hook.objects.get(pk=hook_id)
        test = TestCase.objects.get(pk=test_id)

        hook.tests.add(test)
        serializer1 = HookSerializer(instance=hook)
        return Response(serializer1.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """Delete association between test and hook"""
        hook_id = kwargs['hook']
        test_id = kwargs['test']

        hook = Hook.objects.get(pk=hook_id)
        test = TestCase.objects.get(pk=test_id)

        hook.tests.remove(test)
        return Response(status=status.HTTP_204_NO_CONTENT)
