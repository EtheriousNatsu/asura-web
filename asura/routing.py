# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: routing.py	
@time: 2021/8/18	
"""
from channels.routing import ProtocolTypeRouter, URLRouter

from asura.results.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns)
})
