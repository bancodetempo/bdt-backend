from rest_framework import viewsets, filters

from .serializers import UserSerializer
from .models import CustomUser
from .filters import UserFilter


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name', '=google_drive_spreadsheet_id')
