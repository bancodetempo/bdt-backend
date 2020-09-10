import json
from model_bakery import baker

from rest_framework import status
from rest_framework.test import APITestCase

from user.baker_recipes import user_recipe
from timebank.baker_recipes import account_recipe


class OrderViewSetTestCase(APITestCase):

    def setUp(self):
        self.url = '/api/v0/orders/'

        self.user_a = baker.make_recipe(
            'user.user_recipe', email='user_a@email.com')
        self.user_b = baker.make_recipe(
            'user.user_recipe', email='user_b@email.com')

        self.account_a = baker.make_recipe(
            'timebank.account_recipe', owner=self.user_a, balance=10)
        self.account_b = baker.make_recipe(
            'timebank.account_recipe', owner=self.user_b, balance=10)

    def test_insufficient_funds_returns_400_status_code_with_message(self):

        order_data = {
            'requester': self.user_a.id,
            'grantor': self.user_b.id,
            'order_price': 20,
            'description': 'no tengo plata',
        }
        response = self.client.post(self.url, order_data)

        self.assertEquals(
            response.status_code, status.HTTP_400_BAD_REQUEST
        )
        response_content = json.loads(response.content)
        non_field_errors = response_content['non_field_errors']
        self.assertTrue('Saldo insuficiente' in non_field_errors)
