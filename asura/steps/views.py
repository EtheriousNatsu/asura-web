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

from .models import (
    Setup,
    SetupAndTestCaseIntermediateTable,
    Teardown,
    TeardownAndTestCaseIntermediateTable
)
from .serializers import (
    SetupAndTestCaseIntermediateTableSerializer,
    SetupSerializer,
    TeardownAndTestCaseIntermediateTableSerializer,
    TeardownSerializer
)
from asura.testcases.models import TestCase


class SetupViewSet(ModelViewSet):
    """Setup CRUD"""

    serializer_class = SetupSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Setup.objects.filter(
            service__user__id=self.request.user.pk
        )


class SetupAndTestCaseView(APIView):
    """Setup step view"""

    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        """Create setup step"""

        setup_id = kwargs['setup']
        test_id = kwargs['test']

        setup = Setup.objects.get(pk=setup_id)
        test = TestCase.objects.get(pk=test_id)
        o = SetupAndTestCaseIntermediateTable.objects.create(
            testcase=test,
            setup=setup
        )

        serializer1 = SetupAndTestCaseIntermediateTableSerializer(instance=o)
        return Response(serializer1.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """Delete a setup step"""

        setup_id = kwargs['setup']
        test_id = kwargs['test']

        o = SetupAndTestCaseIntermediateTable.objects.get(
            setup_id=setup_id, testcase_id=test_id)
        o.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TeardownViewSet(ModelViewSet):
    """Teardown CRUD"""

    serializer_class = TeardownSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Teardown.objects.filter(
            service__user__id=self.request.user.pk
        )


class TeardownAndTestCaseView(APIView):
    """Teardown step view"""

    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        """Create a teardown step"""

        teardown_id = kwargs['teardown']
        test_id = kwargs['test']

        teardown = Teardown.objects.get(pk=teardown_id)
        test = TestCase.objects.get(pk=test_id)
        o = TeardownAndTestCaseIntermediateTable.objects.create(
            testcase=test,
            teardown=teardown
        )

        serializer1 = TeardownAndTestCaseIntermediateTableSerializer(
            instance=o)
        return Response(serializer1.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        """Delete a teardown step"""

        teardown_id = kwargs['teardown']
        test_id = kwargs['test']

        o = TeardownAndTestCaseIntermediateTable.objects.get(
            teardown_id=teardown_id,
            testcase_id=test_id)
        o.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
