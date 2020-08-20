from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase


class UserViewSetTestCase(APITestCase):
    endpoint = '/api/v0/users/'

    def setUp(self):
        self.user = baker.make_recipe(
            'user.user_recipe',
            first_name="Arnold",
            last_name="Schwarznegger",
            google_drive_spreadsheet_id="00425",

        )

    def test_search_user_by_first_name_containing(self):
        baker.make_recipe(
            'user.user_recipe',
            first_name="Ricky",
            last_name="Martin",
            google_drive_spreadsheet_id="00421",

        )
        first_name_searched = 'Arnold'
        url_with_parameters = f'{self.endpoint}?search={first_name_searched}'
        response = self.client.get(url_with_parameters)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_content = response.data
        self.assertEquals(len(response_content), 1)
        self.assertEquals(response_content[0]['id'], self.user.id)

    def test_search_user_by_last_name_containing(self):
        baker.make_recipe(
            'user.user_recipe',
            first_name="Ricky",
            last_name="Martin",
            google_drive_spreadsheet_id="00421",

        )
        last_name_search_parameter = "Schwarz"
        url_with_parameters = f'{self.endpoint}?search={last_name_search_parameter}'
        response = self.client.get(url_with_parameters)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_content = response.data
        self.assertEquals(len(response_content), 1)
        self.assertEquals(response_content[0]['id'], self.user.id)

    def test_search_user_by_google_drive_exact_value(self):
        baker.make_recipe(
            'user.user_recipe',
            first_name="Ricky",
            last_name="Martin",
            google_drive_spreadsheet_id="00421",

        )
        google_drive_spreadsheet_id_search_value = "00425"
        url_with_parameters = f'{self.endpoint}?search={google_drive_spreadsheet_id_search_value}'
        response = self.client.get(url_with_parameters)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_content = response.data
        self.assertEquals(len(response_content), 1)
        self.assertEquals(response_content[0]['id'], self.user.id)

    def test_search_user_by_google_drive_only_containing_value_doesnt_return(self):
        """
        User has to type in exact same value in order
        to return a record
        """
        baker.make_recipe(
            'user.user_recipe',
            first_name="Ricky",
            last_name="Martin",
            google_drive_spreadsheet_id="00421",

        )
        google_drive_spreadsheet_id_search_value = "0042"
        url_with_parameters = f'{self.endpoint}?search={google_drive_spreadsheet_id_search_value}'

        response = self.client.get(url_with_parameters)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_content = response.data
        self.assertEquals(len(response_content), 0)
