# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: views.py	
@time: 2021/8/17	
"""

from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from asura.utils.response import ResponseOk
from asura.core.testsuite import RunnableTestSuite
from asura.steps.models import (
    SetupAndTestCaseIntermediateTable,
    TeardownAndTestCaseIntermediateTable
)
from asura.steps.serializers import (
    SetupAndTestCaseIntermediateTableSerializer,
    TeardownAndTestCaseIntermediateTableSerializer
)
from .models import TestCase
from .serializers import TestCaseSerializer
from asura.testsuites.models import TestSuite


class TestCaseViewSet(ModelViewSet):
    """TestCase CRUD"""

    serializer_class = TestCaseSerializer
    permission_classes = [IsAuthenticated, ]

    @action(detail=True, methods=['get'])
    def steps(self, request, pk=None):
        """Steps view"""

        setups = SetupAndTestCaseIntermediateTable.objects.filter(
            testcase_id=pk)
        teardowns = TeardownAndTestCaseIntermediateTable.objects.filter(
            testcase_id=pk)
        serializer1 = SetupAndTestCaseIntermediateTableSerializer(
            instance=setups, many=True)
        serializer2 = TeardownAndTestCaseIntermediateTableSerializer(
            instance=teardowns, many=True)
        return Response(
            {
                'setups': serializer1.data,
                'teardowns': serializer2.data,
                'test': pk
            }
        )

    @steps.mapping.put
    def put_steps(self, request, pk=None):
        """steps order view"""

        test_id = int(request.data['test'])
        setups = request.data['setups']
        teardowns = request.data['teardowns']

        for setup in setups:
            o1 = SetupAndTestCaseIntermediateTable.objects.get(
                Q(setup_id=setup["id"]) & Q(testcase_id=test_id)
            )
            o1.step_number = setup["step_number"]
            o1.save()

        for teardown in teardowns:
            o2 = TeardownAndTestCaseIntermediateTable.objects.get(
                Q(teardown_id=teardown["id"]) & Q(testcase_id=test_id)
            )
            o2.step_number = teardown["step_number"]
            o2.save()

        return Response(
            data=request.data
        )

    @action(detail=True, methods=['post', 'get'])
    def run(self, request, pk=None):
        """Run a single test"""
        tests = TestCase.objects.filter(pk=pk)

        if tests:
            RunnableTestSuite(request, tests).run()
            return ResponseOk()
        else:
            data = {
                "code": "InvalidRequestError",
                "message": "At least one tests must be triggered."
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return TestCase.objects.filter(
            service__user__id=self.request.user.pk
        )
