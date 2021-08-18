# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: asgi.py	
@time: 2021/8/18	
"""
import os
from configurations import importer
from channels.asgi import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asura.config")
os.environ.setdefault("DJANGO_CONFIGURATION", "Production")

importer.install()

channel_layer = get_channel_layer()
