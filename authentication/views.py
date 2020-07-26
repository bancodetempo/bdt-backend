from django.shortcuts import render
from rest_framework  import status, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import AuthenticationSerializer
from .models import CustomUser


class AuthenticationViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = CustomUser.objects.all()
    serializer_class = AuthenticationSerializer

    @action(methods=['put'], detail=False)
    def request_user_validation(self, request):
        data = request.data
        user = CustomUser.objects.get(google_drive_spreadsheet_id=data.get('google_drive_spreadsheet_id'))
        serializer = AuthenticationSerializer(user, data=data, partial=True)

        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)
        return Response(serializer.data)
