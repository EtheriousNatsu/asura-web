# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: views.py	
@time: 2021/8/17	
"""
from urllib.parse import urlparse

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import ServiceSerializer
from .models import Service
from asura.utils.response import ResponseOk
from asura.environments.models import Environment
from asura.environments.serializers import EnvironmentSerializer
from asura.testcases.models import TestCase
from asura.testcases.serializers import TestCaseSerializer
from asura.assertions.models import Assertion
from asura.assertions.serializers import AssertionSerializer
from asura.core.testsuite import RunnableTestSuite


class ImportViewSet(APIView):
    """New Service"""
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        # todo 代码写的很乱，有时间在优化
        user_id = request.data.get('account')
        import_type = request.data.get('type')
        url = request.data.get('url')

        self.user = request.user
        self._parse_url(url)

        data = self._import_url()

        return Response(data=data)

    def _parse_url(self, url):
        o = urlparse(url)
        self.scheme = o.scheme
        self.host = o.netloc
        self.path = o.path if o.path else '/'

    def _import_url(self):
        service = Service.objects.create(
            name=self.host,
            schemes=self.scheme,
            host=self.host,
            icon="http://statics.dnspod.cn/proxy_favicon/_/favicon?domain=" + self.host,
            user=self.user
        )
        services_data = ServiceSerializer([service], many=True).data

        environment = Environment.objects.create(
            name="production",
            url=self.host,
            service=service
        )
        environments_data = EnvironmentSerializer([environment], many=True).data

        test = TestCase.objects.create(
            description='Ensure the HTTP request returns a 200 OK',
            endpoint=self.path,
            service=service,
        )
        tests_data = TestCaseSerializer([test], many=True).data

        assertion = Assertion.objects.create(
            comparator="AssertEquals",
            source="AssertStatusCode",
            target="200",
            test=test
        )
        assertions_data = AssertionSerializer([assertion], many=True).data

        data = {
            "services": services_data,
            "assertions": assertions_data,
            "environments": environments_data,
            "tests": tests_data
        }

        return data


class ServiceViewSet(ModelViewSet):
    """Service CRUD"""

    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Service.objects.filter(user_id=self.request.user.pk)

    @action(detail=True, methods=['post', 'get'])
    def run(self, request, pk=None):
        tests = TestCase.objects.filter(service=pk)

        if tests:
            RunnableTestSuite(request, tests).run()
            return ResponseOk()
        else:
            data = {
                "code": "InvalidRequestError",
                "message": "At least one tests must be triggered."
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
