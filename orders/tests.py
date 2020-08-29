from decimal import Decimal
from django.test import TestCase
from model_bakery import baker

from user.baker_recipes import user_recipe
from timebank.baker_recipes import account_recipe

from .models import Order


class OrderTestCase(TestCase):

    def setUp(self):
        self.user_a = baker.make_recipe(
            'user.user_recipe', email='user_a@email.com')
        self.user_b = baker.make_recipe(
            'user.user_recipe', email='user_b@email.com')

        self.account_a = baker.make_recipe(
            'timebank.account_recipe', owner=self.user_a, balance=10)
        self.account_b = baker.make_recipe(
            'timebank.account_recipe', owner=self.user_b, balance=10)

    def test_confirm_order_turns_it_to_confirmed_and_executes_transaction(self):
        order = baker.make(
            Order,
            requester=self.user_a,
            grantor=self.user_b,
            order_price=5
        )
        Order.confirm_order(order.uid)
        order.refresh_from_db()
        self.account_a.refresh_from_db()
        self.account_b.refresh_from_db()
        self.assertEquals(order.status, 1)
        self.assertEquals(self.account_a.balance, Decimal(5))
        self.assertEquals(self.account_b.balance, Decimal(15))
