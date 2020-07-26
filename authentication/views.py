from django.shortcuts import render
from rest_framework  import status, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import AuthenticationSerializer
from .models import CustomUser

from .mailers import ConfirmUserRegistrationMail


class AuthenticationViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = CustomUser.objects.all()
    serializer_class = AuthenticationSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        ConfirmUserRegistrationMail.send_to([instance.email])

    @action(methods=['put'], detail=False)
    def request_user_validation(self, request):
        data = request.data
        user = CustomUser.objects.get(google_drive_spreadsheet_id=data.get('google_drive_spreadsheet_id'))
        serializer = AuthenticationSerializer(user, data=data, partial=True)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
