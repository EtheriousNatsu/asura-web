# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: urls.py	
@time: 2021/8/17	
"""
from django.urls import path

from .views import *


urlpatterns = [
    path('signup', SignupView.as_view()),
    path('login', LoginView.as_view()),
    path('reset', PasswordResetView.as_view()),
    path('reset/<token>/<uidb64>', PasswordResetConfirmView.as_view()),
]
