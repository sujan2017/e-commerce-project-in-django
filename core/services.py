from django.core.mail import send_mail
from django.conf import settings
from .models import Notification, EmailLog


# reusable business logic inside a service layer

def create_notification(user, message):

    # create notification for a user

    Notification.objects.create(
        user=user,
        message=message
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