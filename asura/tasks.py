# encoding: utf-8
"""
@author: John
@contact: zhouqiang847@gmail.com
@file: tasks.py	
@time: 2021/8/17	
"""
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template import loader


@shared_task
def send_email(subject_template_name, email_template_name, context,
               from_email, to_email, html_email_template_name=None):
    """发送邮件"""
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    if email_template_name is not None:
        body = loader.render_to_string(email_template_name, context)
    else:
        body = ''

    email_message = EmailMultiAlternatives(
        subject, body, from_email, to_email)
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')

    email_message.send()
