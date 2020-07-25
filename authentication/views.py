from django.shortcuts import render
from rest_framework  import status, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import AuthencationSerializer

from .models import CustomUser

class AuthenticationViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = CustomUser.objects.all()
    serializer_class = AuthencationSerializer

    @action(methods=['put'], detail=False)
    def request_user_validation(self, request):
        data = request.data
        #import ipdb; ipdb.set_trace();
        user = CustomUser.objects.get(google_drive_spreadsheet_id=data.get('google_drive_spreadsheet_id'))
        user.email = data.get('email')
        user.save()
        return Response('', status=status.HTTP_200_OK)
