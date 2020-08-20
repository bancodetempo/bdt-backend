from django.db import models
from decouple import config
from django.core.mail import send_mail
from django.conf import settings


class ConfirmUserRegistrationMail:
    subject = 'Confirme seu cadastro'
    message = "Por favor confirme seu email"
    from_email = settings.SMTP_USERNAME

    @classmethod
    def send_to(cls, emails):
        send_mail(subject=cls.subject,
                  message=cls.message,
                  from_email=settings.SMTP_USERNAME,
                  recipient_list=emails)
