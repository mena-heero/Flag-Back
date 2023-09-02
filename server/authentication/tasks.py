import math

from django.apps import apps
from celery import shared_task

from .emails import *


@shared_task(name="otp_email_task")
def otp_email_queue(email, otp, reason):
    send_otp_email(email, otp, reason)


@shared_task(name="verify_confirm_email_task")
def verify_confirm_email_queue(email):
    send_verify_confirm_email(email)
