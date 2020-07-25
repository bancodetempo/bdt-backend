from rest_framework import serializers
from .models import CustomUser

class AuthencationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'google_drive_spreadsheet_id']

        def update(self, validated_data):
            user = super().update(user, validated_data)
            return user


