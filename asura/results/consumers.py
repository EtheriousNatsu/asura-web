# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: consumers.py	
@time: 2021/8/18	
"""
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ResultConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['token']
        self.room_group_name = 'asura_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group

    def process_case_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'type': 'case'
        }))

    def process_suite_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'type': 'suite'
        }))

    def process_schedule_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'type': 'schedule'
        }))
