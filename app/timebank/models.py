import uuid

from django.db import models
from django.contrib.auth import get_user_model


class Account(models.Model):

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'

    id = models.AutoField(primary_key=True)
    uid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='Identificador Público'
    )
    owner = models.OneToOneField(
        get_user_model(),
        on_delete=models.PROTECT
    )
    balance = models.IntegerField(
        verbose_name='Saldo atual'
    )

