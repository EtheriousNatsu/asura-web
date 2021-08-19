# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: asgi.py	
@time: 2021/8/18	
"""

import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asura.config.production')
django.setup()
application = get_default_application()
