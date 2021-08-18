import os

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import django.dispatch
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from asura.tasks import send_email

# 重置密码
reset_password = django.dispatch.Signal(providing_args=['user', ])


@receiver(
    reset_password,
    dispatch_uid="send_reset_password_email"
)
def send_account_related_email(sender, user, **kwargs):
    """
    发送重置密码和用户激活邮件
    """
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk)).decode()
    url = sender.url.format(
        service_host=os.getenv('SERVICE_HOST'),
        token=token,
        uidb64=uidb64
    )
    context = {
        'url': url
    }

    send_email.delay(
        subject_template_name=sender.subject_template_name,
        email_template_name=None,
        context=context,
        from_email=os.getenv("EMAIL_HOST_USER"),
        to_email=[user.email, ],
        html_email_template_name=sender.html_email_template_name
    )


@receiver(
    post_save,
    sender=settings.AUTH_USER_MODEL,
    dispatch_uid="create_auth_token"
)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """用户注册成功后，同时创建token"""
    if created:
        Token.objects.create(user=instance)


