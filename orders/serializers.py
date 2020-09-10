from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('requester', 'grantor', 'order_price', 'description')

    def validate(self, attrs):
        requester = attrs['requester']
        order_price = attrs['order_price']

        requester_account_balance = requester.account.balance

        if requester_account_balance < order_price:
            raise serializers.ValidationError('Saldo insuficiente')
