from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.IntegerField(required=False)

    class Meta:
        model = Order
        fields = '__all__'
