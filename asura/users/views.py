# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: views.py	
@time: 2021/8/16	
"""
import os

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from asura.utils.response import ResponseOk
from .models import User
from .signals import reset_password
from .serializers import (
    UserSerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    EmailSerializer
)


class SignupView(APIView):
    """用户注册"""
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        auth_token = Token.objects.get(user=serializer.instance)
        data = dict(
            list(serializer.data.items()) +
            [('token', auth_token.key)]
        )

        return ResponseOk(data, status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):
    """用户登录"""

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        auth_token = Token.objects.get(user=user)
        data = dict(
            list(UserSerializer(user).data.items()) +
            [('token', auth_token.key)]
        )

        return ResponseOk(data)


class PasswordResetView(APIView):
    """用户重置密码邮件"""

    serializer_class = EmailSerializer
    subject_template_name = 'email/user_reset_password.txt'
    html_email_template_name = 'email/user_reset_password.html'
    url = '{service_host}/account/{token}/resetpassword/{uidb64}'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_password.send(
            sender=self.__class__,
            user=serializer.validated_data['user']
        )

        return ResponseOk()


class PasswordResetConfirmView(APIView):
    """用户重置密码"""

    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        uid_b64 = kwargs['uidb64']
        token = kwargs['token']

        user = self.get_user(uid_b64)

        if user and default_token_generator.check_token(user, token):
            serializer = self.serializer_class(instance=user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return ResponseOk()
        else:
            data = {'code': 1, 'msg': '链接失效，请重新进行发送重置密码邮件操作'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_user(uid_b64):
        try:
            uid = urlsafe_base64_decode(uid_b64).decode()
            user = User.objects.get(pk=uid)
        except (
                TypeError,
                ValueError,
                OverflowError,
                User.DoesNotExist,
                ValidationError
        ):
            user = None
        return user
