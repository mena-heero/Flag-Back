import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMultiAlternatives, get_connection, send_mail
from django.template.loader import render_to_string
from decouple import config


def send_signup_email(email):
    subject = "Signup Successful to Flagedu."

    from_email = config("FLAGEDU_EMAIL")
    to = email
    text_content = " "
    html_content = """
    <p>Hi,</p>
    <p>Congratulations! You just registered to Flagedu!</p>
    <br>
    <p>Sincerely,</p>
    <p>Flagedu Team</p>
    """
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_otp_email(email, otp, reason):

    subject = "OTP for Flagedu."

    from_email = config("FLAGEDU_EMAIL")
    to = email

    msg_html = render_to_string(
        "account/otp_email.html", {"otp": otp, "reason": reason}
    )
    text_content = " "

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(msg_html, "text/html")
    msg.send()


def send_verify_confirm_email(email):
    subject = "You have successfully verified your Flagedu account!"

    from_email = config("FLAGEDU_EMAIL")
    to = email

    msg_html = render_to_string("account/account_verify_email.html", {})
    text_content = " "

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(msg_html, "text/html")
    msg.send()
