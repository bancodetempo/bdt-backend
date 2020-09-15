from decimal import Decimal

from rest_framework import serializers
from .models import Order


def validate_same_requester(requester_id: int, grantor_id: int) -> None:
    if requester_id == grantor_id:
        raise serializers.ValidationError(
            'Não é possível solicitar troca de horas para si mesma(o)')


def validate_requester_balance(requester_account_balance: Decimal, order_price: Decimal) -> None:
    if requester_account_balance < order_price:
        raise serializers.ValidationError('Saldo insuficiente')


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('requester', 'grantor', 'order_price', 'description')

    def validate(self, attrs):
        requester = attrs['requester']
        grantor = attrs['grantor']
        order_price = attrs['order_price']

        requester_account_balance = requester.account.balance

        validate_same_requester(requester.id, grantor.id)
        validate_requester_balance(requester_account_balance, order_price)

        return attrs
