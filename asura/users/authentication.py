# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: authentication.py
@time: 2021/8/16
"""
from rest_framework import authentication, exceptions
from rest_framework.authtoken.models import Token

from .models import User
from .constants import CUSTOM_AUTH_FAIL


class Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        key = request.query_params.get('api_token')
        if not key:
            return None

        try:
            token = Token.objects.get(key=key)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(CUSTOM_AUTH_FAIL)
        return token.user, token
