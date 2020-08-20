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
            'timebank.account_recipe', owner=self.user_a)
        self.account_b = baker.make_recipe(
            'timebank.account_recipe', owner=self.user_b)

    def test_confirm_order_turns_it_to_confirmed(self):
        order = baker.make(Order, requester=self.user_a, grantor=self.user_b)
        Order.confirm_order(order.uid)
