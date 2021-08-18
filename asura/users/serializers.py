# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: serializers.py
@time: 2021/8/16
"""

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate


from .models import User
from .constants import *


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(
        max_length=8,
        min_length=6,
        write_only=True,
        error_messages=PASSWORD_ERROR_MESSAGES
    )
    email = serializers.CharField(
        max_length=254,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=EMAIL_ALREADY_EXISTS
            )
        ],
        error_messages={}
    )

    def create(self, validated_data):
        return User.objects.create(
            email=validated_data['email'],
            username=validated_data['email'],
            password=make_password(validated_data['password'])
        )

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class PasswordResetConfirmSerializer(serializers.Serializer):
    password1 = serializers.CharField(
        max_length=8,
        min_length=6,
        write_only=True,
        error_messages=PASSWORD_ERROR_MESSAGES
    )
    password2 = serializers.CharField(
        max_length=8,
        min_length=6,
        write_only=True,
        error_messages=PASSWORD_ERROR_MESSAGES
    )

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise serializers.ValidationError(INCONSISTENT_PASSWORDS)

        return attrs

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data['password1'])
        instance.save()

        return instance


class EmailSerializer(serializers.Serializer):

    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')

        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError(EMAIL_NOT_REGISTERED)
        else:
            raise serializers.ValidationError(EMAIL_NOT_BE_EMPTY, code='required')

        attrs['user'] = user
        return attrs


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            if not user:
                raise serializers.ValidationError(AUTH_FAIL, code='authorization')
        else:
            raise serializers.ValidationError(AUTH_NOT_BE_EMPTY, code='authorization')

        attrs['user'] = user
        return attrs
