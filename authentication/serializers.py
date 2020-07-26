from rest_framework import serializers
from .models import CustomUser


class AuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'google_drive_spreadsheet_id']

