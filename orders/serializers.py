from decimal import Decimal

from rest_framework import serializers

from timebank.models import Account
from .models import Order


def validate_requester_account(attr) -> None:
    if not Account.objects.filter(owner=attr).exists():
        raise serializers.ValidationError(
            'É necessário criar uma conta para a(o) solicitante')


def validate_grantor_account(attr) -> None:
    if not Account.objects.filter(owner=attr).exists():
        raise serializers.ValidationError(
            'É necessário criar uma conta para o(a) prestador(a) de serviço/produto')


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

        validate_requester_account(requester)
        requester_account_balance = requester.account.balance

        validate_same_requester(requester.id, grantor.id)

        validate_grantor_account(grantor)

        validate_requester_balance(requester_account_balance, order_price)

        return attrs
