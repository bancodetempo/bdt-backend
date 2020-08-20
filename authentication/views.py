from rest_framework import viewsets
from django_filters import rest_framework as filters

from .serializers import AuthenticationSerializer
from .models import CustomUser
from .filters import UserFilter


class AuthenticationViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = CustomUser.objects.all()
    serializer_class = AuthenticationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter
