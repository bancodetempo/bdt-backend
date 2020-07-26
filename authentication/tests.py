from django.test import TestCase
from rest_framework.test import APITestCase

from authentication.models import CustomUser

class AuthenticationViewSetTest(APITestCase):

    def test_update(self):
        google_drive_spreadsheet_id = '123'
        email = 'test@email.com'
        CustomUser.objects.create(google_drive_spreadsheet_id=google_drive_spreadsheet_id)
        user = CustomUser.objects.get(google_drive_spreadsheet_id=google_drive_spreadsheet_id)
        response = self.client.put('/api/v0/authentication/request_user_validation/',
                                   { "email": email,
                                    'google_drive_spreadsheet_id': google_drive_spreadsheet_id },
                                   format="json")
        user = CustomUser.objects.get(google_drive_spreadsheet_id=google_drive_spreadsheet_id)
        self.assertEqual(user.email, email)
        self.assertEqual(response.status_code, 200)

