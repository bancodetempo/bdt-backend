import uuid
from decimal import Decimal

from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from orders.models import Order


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
    balance = models.DecimalField(
        verbose_name='Saldo',
        decimal_places=1,
        max_digits=5,
    )
    owner = models.OneToOneField(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        account_name = '{} - {}H'.format(str(self.owner), str(self.balance))
        return account_name

    @classmethod
    def deposit(cls, user, amount, reference=None):
        with transaction.atomic():
            account = cls.objects.select_for_update().get(owner=user)
            account.balance += Decimal(amount)
            account.save()

            AccountTransaction.create(
                account=account,
                transaction_type=AccountTransaction.TRANSACTION_TYPE_IN,
                delta=amount,
                reference=reference,
                balance_after_transaction=account.balance,
            )

    @classmethod
    def withdraw(cls, user, amount, reference=None):
        with transaction.atomic():
            account = cls.objects.select_for_update().get(owner=user)
            # TODO:  Put validation to check for sufficient funds
            account.balance -= Decimal(amount)
            account.save()

            AccountTransaction.create(
                account=account,
                transaction_type=AccountTransaction.TRANSACTION_TYPE_OUT,
                delta=amount,
                reference=reference,
                balance_after_transaction=account.balance,
            )

    @classmethod
    def create_user_with_account(cls, user_email, password=None):
        user_model = get_user_model()
        new_user = user_model.create_user(
                user_email,
                password,
                is_active=False,
                is_staff=False,
            )

        created_account = cls.objects.create(
            balance=0,
            owner=new_user,
        )
        return created_account, new_user


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
        primary_key=True,
    )
    account = models.ForeignKey(
        Account,
        verbose_name='Conta',
        on_delete=models.PROTECT,
    )
    transaction_type = models.IntegerField(
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name='Tipo de transação'
    )
    delta = models.DecimalField(
        verbose_name='Valor da transação',
        decimal_places=1,
        max_digits=5,
        help_text='Valor da transação',
    )
    reference = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        null=True,
    )
    balance_after_transaction = models.DecimalField(
        verbose_name='Saldo depois da transação',
        decimal_places=1,
        max_digits=5,
        help_text='Saldo depois da transação',
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        transaction_type = self.get_transaction_type_display()
        transaction_name = '{} {} {}'.format(self.delta, transaction_type, self.account.owner.email)
        return transaction_name

    @classmethod
    def create(cls, account, transaction_type, delta, reference, balance_after_transaction):
        return cls.objects.create(
            account=account,
            transaction_type=transaction_type,
            delta=delta,
            reference=reference,
            balance_after_transaction=balance_after_transaction,
        )
