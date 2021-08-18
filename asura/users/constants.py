# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: constants.py	
@time: 2021/8/16
"""
from django.utils.translation import gettext_lazy as _


PASSWORD_ERROR_MESSAGES = {
    'min_length': _('密码长度不能少于6位'),
    'max_length': _('密码长度不能超过8位'),
    'blank': _('密码不能为空')
}

EMAIL_ALREADY_EXISTS = _('邮箱已存在')

INCONSISTENT_PASSWORDS = _('密码不一致')

EMAIL_NOT_REGISTERED = _('邮箱未注册')

EMAIL_NOT_BE_EMPTY = _('邮箱不能为空')

AUTH_FAIL = _('您输入的账号或密码有误，请重新输入')

AUTH_NOT_BE_EMPTY = _('邮箱和密码不能为空')

CUSTOM_AUTH_FAIL = _('Token无效')

LINK_INVALID = _('链接无效，请重新发送重置密码邮件')
