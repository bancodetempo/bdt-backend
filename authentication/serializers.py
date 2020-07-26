from rest_framework import serializers
from .models import CustomUser
from .mailers import ConfirmUserRegistrationMail


class AuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'google_drive_spreadsheet_id']

        def perform_update(self, serializer):
            instance = serializer.save()
            ConfirmUserRegistrationMail.send_to([instance.email])


