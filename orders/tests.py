from django.test import TestCase
from model_mommy import mommy

from authentication.test_recipes import user_recipe
from timebank.test_recipes import account_recipe

from .models import Order


class OrderTestCase(TestCase):

    def setUp(self):
        self.user_a = user_recipe.make(email='user_a@email.com')
        self.user_b = user_recipe.make(email='user_b@email.com')

        self.account_a = account_recipe.make(owner=self.user_a)
        self.account_b = account_recipe.make(owner=self.user_b)

    def test_confirm_order_turns_it_to_confirmed(self):
        order = mommy.make(Order, requester=self.user_a, grantor=self.user_b)
        Order.confirm_order(order.uid)

