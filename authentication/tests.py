import json

from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationViewSetTest(APITestCase):
    endpoint = '/api/v0/authentication/'

    def setUp(self):
        self.user = baker.make_recipe(
            'authentication.user_recipe',
            first_name="Arnold",
            last_name="Schwarznegger",
            google_drive_spreadsheet_id="00425",

        )

    def test_search_user_by_first_name(self):
        baker.make_recipe(
            'authentication.user_recipe',
            first_name="Ricky",
            last_name="Martin",
            google_drive_spreadsheet_id="00421",

        )
        url_with_parameters = "{}?search={}".format(self.endpoint, "Arnold")
        response = self.client.get(url_with_parameters)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content)
        self.assertEquals(len(response_content), 1)
        self.assertEquals(response_content[0]['id'], self.user.id)

    def test_search_user_by_last_name_containing(self):
        baker.make_recipe(
            'authentication.user_recipe',
            first_name="Ricky",
            last_name="Martin",
            google_drive_spreadsheet_id="00421",

        )
        url_with_parameters = "{}?search={}".format(
            self.endpoint, "Schwarz")
        response = self.client.get(url_with_parameters)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content)
        self.assertEquals(len(response_content), 1)
        self.assertEquals(response_content[0]['id'], self.user.id)

    def test_search_user_by_google_drive_exact_value(self):
        baker.make_recipe(
            'authentication.user_recipe',
            first_name="Ricky",
            last_name="Martin",
            google_drive_spreadsheet_id="00421",

        )
        url_with_parameters = "{}?search={}".format(
            self.endpoint, "00425")
        response = self.client.get(url_with_parameters)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content)
        self.assertEquals(len(response_content), 1)
        self.assertEquals(response_content[0]['id'], self.user.id)

    def test_search_user_by_google_drive_only_containing_value_doesnt_return(self):
        """
        User has to type in exact same value in order
        to return a record
        """
        baker.make_recipe(
            'authentication.user_recipe',
            first_name="Ricky",
            last_name="Martin",
            google_drive_spreadsheet_id="00421",

        )
        url_with_parameters = "{}?search={}".format(
            self.endpoint, "0042")
        response = self.client.get(url_with_parameters)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_content = json.loads(response.content)
        self.assertEquals(len(response_content), 0)
