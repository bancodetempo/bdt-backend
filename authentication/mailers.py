from django.db import models
from decouple import config

class ConfirmUserRegistrationMail:
        subject = 'Confirme seu cadastro'
        message = "Por favor confirme seu email"
        from_email = config('SMTP_USERNAME')

        @classmethod
        def send_to(cls, emails):
            send_mail(subject=cls.subject,
                      message=cls.message,
                      from_email=config('SMTP_USERNAME'),
                      recipient_list=emails)


