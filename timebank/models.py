import uuid

from django.db import models
from django.contrib.auth import get_user_model


class Account(models.Model):

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas de usuários'

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
        verbose_name='Saldo'
    )

class AccountTransaction(models.Model):

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'

    TRANSACTION_TYPE_IN = 0
    TRANSACTION_TYPE_OUT = 1

    TRANSACTION_TYPE_CHOICES = (
        (TRANSACTION_TYPE_IN, 'Entrada'),
        (TRANSACTION_TYPE_OUT, 'Saída')
    )

    id = models.AutoField(
        primary_key=True
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT
    )
    transaction_type = models.IntegerField(
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name='Tipo de transação'
    )
    delta = models.IntegerField(
        help_text='Delta do saldo'
    )
    reference = models.TextField(
        blank=False
    )
    debug_balace = models.IntegerField(
        help_text='Saldo depois da transação'
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

