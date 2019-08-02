from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from model_mommy import mommy

from .models import Account


class AccountTestCase(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model(), email='teste@email.com')

    def test_deposit_into_account(self):
        mommy.make(Account, owner=self.user, balance=0)
        Account.deposit(self.user, 1.5)
        self.user.account.refresh_from_db()
        self.assertEqual(self.user.account.balance, 1.5)

    def test_withdraw_from_account(self):
        mommy.make(Account, owner=self.user, balance=1.5)
        Account.withdraw(self.user, 1.5)
        self.user.account.refresh_from_db()
        self.assertEqual(self.user.account.balance, 0)
