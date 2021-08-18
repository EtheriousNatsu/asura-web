import os
from os.path import join

from .common import Common, BASE_DIR


class Production(Common):
    INSTALLED_APPS = Common.INSTALLED_APPS
    # Site
    # https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ["*"]

    # Email
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = os.getenv('EMAIL_PORT')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    EMAIL_USE_SSL = True

    # Static file
    STATICFILES_DIRS = [
        Common.STATIC_ROOT
    ]

    STATIC_URL = os.getenv('STATIC_URL')
