from celery import shared_task
 
from django.conf import settings
from django.core.mail import send_mail
 
@shared_task
def task_send_email(subject, message, send_to):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [send_to]
    )
    print('Mail is sent!')
 