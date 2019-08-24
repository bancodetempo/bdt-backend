from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ViewSetMixin

from .serializers import OrderSerializer
from .models import Order


class OrderViewSet(ViewSetMixin, ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer