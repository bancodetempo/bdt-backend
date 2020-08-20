from rest_framework import viewsets
from django_filters import rest_framework as filters

from .serializers import UserSerializer
from .models import CustomUser
from .filters import UserFilter


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter
