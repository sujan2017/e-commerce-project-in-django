from django.core.mail import send_mail
from django.conf import settings
from .models import Notification, EmailLog


# reusable business logic inside a service layer

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def create_notification(user, message):
    Notification.objects.create(user=user, message=message)

    channel_layer = get_channel_layer()
    group_name = f"user_{user.id}"

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",
            "message": message,
        }
    )


def send_email_and_log(subject,message, to_email):

    #send email and log into database

    send_mail(
        subject, 
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=True
    )

    EmailLog.objects.create(
        to_email=to_email,
        subject=subject
    )