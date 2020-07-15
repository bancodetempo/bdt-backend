from decimal import Decimal

from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Account(models.Model):

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas de usuários'

    id = models.AutoField(primary_key=True)
    balance = models.DecimalField(
        verbose_name='Saldo',
        decimal_places=1,
        max_digits=5,
    )
    owner = models.OneToOneField(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='account',
    )

    def __str__(self):
        account_name = '{} - {}H'.format(str(self.owner), str(self.balance))
        return account_name

    @classmethod
    def deposit(cls, user, amount):
        with transaction.atomic():
            account = cls.objects.select_for_update().get(owner=user)
            account.balance += Decimal(amount)
            account.save()

            AccountTransaction.create(
                account=account,
                transaction_type=AccountTransaction.TRANSACTION_TYPE_IN,
                delta=amount,
                balance_after_transaction=account.balance,
            )

    @classmethod
    def withdraw(cls, user, amount):
        with transaction.atomic():
            account = cls.objects.select_for_update().get(owner=user)
            # TODO:  Put validation to check for sufficient funds
            account.balance -= Decimal(amount)
            account.save()

            AccountTransaction.create(
                account=account,
                transaction_type=AccountTransaction.TRANSACTION_TYPE_OUT,
                delta=amount,
                balance_after_transaction=account.balance,
            )

    @classmethod
    def create_user_with_account(cls, user_object, balance):
        user_model = get_user_model()

        if 'password' in user_object:
            password = user_object.pop('password')

        new_user = user_model.objects.create(
            **user_object,
        )

        if password:
            new_user.set_password(password)
            new_user.save()

        created_account = cls.objects.create(
            balance=0,
            owner=new_user,
        )
        created_account.deposit(user=new_user, amount=balance)
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
        transaction_name = '{} {} {}'.format(
            self.delta, transaction_type, self.account.owner.email)
        return transaction_name

    @classmethod
    def create(cls, account, transaction_type, delta, balance_after_transaction):
        return cls.objects.create(
            account=account,
            transaction_type=transaction_type,
            delta=delta,
            balance_after_transaction=balance_after_transaction,
        )
