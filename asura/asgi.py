# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: asgi.py	
@time: 2021/8/18	
"""
import os
import configurations
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "asura.config")
os.environ.setdefault("DJANGO_CONFIGURATION", "Production")
configurations.setup()

application = get_default_application()
