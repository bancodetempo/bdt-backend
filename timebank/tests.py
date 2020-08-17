from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from model_bakery import baker
from model_bakery.recipe import Recipe, foreign_key


from .models import Account, AccountTransaction


class AccountTestCase(TestCase):

    def setUp(self):
        self.user = baker.make(get_user_model(), email='teste@email.com')

    def test_deposit_into_account(self):
        baker.make(Account, owner=self.user, balance=0)
        Account.deposit(self.user, 1.5)
        self.user.account.refresh_from_db()
        self.assertEqual(self.user.account.balance, 1.5)
        transaction = AccountTransaction.objects.first()
        self.assertEqual(transaction.transaction_type,
                         AccountTransaction.TRANSACTION_TYPE_IN)
        self.assertEqual(transaction.delta, 1.5)
        self.assertEqual(transaction.account, self.user.account)
        self.assertEqual(transaction.balance_after_transaction,
                         self.user.account.balance)

    def test_withdraw_from_account(self):
        baker.make(Account, owner=self.user, balance=1.5)
        Account.withdraw(self.user, 1.5)
        self.user.account.refresh_from_db()
        self.assertEqual(self.user.account.balance, 0)
        transaction = AccountTransaction.objects.first()
        self.assertEqual(transaction.transaction_type,
                         AccountTransaction.TRANSACTION_TYPE_OUT)
        self.assertEqual(transaction.delta, 1.5)
        self.assertEqual(transaction.account, self.user.account)
        self.assertEqual(transaction.balance_after_transaction,
                         self.user.account.balance)

    def test_create_user_with_account(self):
        new_user_email = 'test@user.com'
        user_object = {
            'email': new_user_email,
            'password': 'dontreallyknow'
        }
        Account.create_user_with_account(user_object)
        self.assertEqual(Account.objects.count(), 1)
        user_account = Account.objects.first()
        user_model = get_user_model()
        created_user = user_model.objects.filter(email=new_user_email)
        self.assertEqual(created_user.count(), 1)
        self.assertEqual(user_account.owner, created_user.first())
