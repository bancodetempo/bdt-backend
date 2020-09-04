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
        search_token = 'Arnold'
        url_with_parameters = f'{self.endpoint}?search={search_token}'
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
        search_token = "Schwarz"
        url_with_parameters = f'{self.endpoint}?search={search_token}'
        response = self.client.get(url_with_parameters)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_content = response.data
        self.assertEquals(len(response_content), 1)
        self.assertEquals(response_content[0]['id'], self.user.id)

    def test_search_user_by_full_name_containing(self):
        baker.make_recipe(
            'user.user_recipe',
            first_name="Ricky",
            last_name="Martin",
            google_drive_spreadsheet_id="00421",

        )
        search_token = "Arn Schwarz"
        url_with_parameters = f'{self.endpoint}?search={search_token}'
        response = self.client.get(url_with_parameters)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_content = response.data
        self.assertEquals(len(response_content), 1)
        self.assertEquals(response_content[0]['id'], self.user.id)

    def test_search_user_by_first_name_containing_and_part_of_last_name_containing(self):
        search_token = "Arn Schw"
        url_with_parameters = f'{self.endpoint}?search={search_token}'
        response = self.client.get(url_with_parameters)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_content = response.data
        self.assertEquals(len(response_content), 1)
        self.assertEquals(response_content[0]['id'], self.user.id)

    def test_search_user_by_last_name_big_name(self):
        user_big_name = baker.make_recipe(
            'user.user_recipe',
            first_name="Ricardo",
            last_name="Monteiro e Lima",
            google_drive_spreadsheet_id="00421",

        )
        search_token = "Lima"
        url_with_parameters = f'{self.endpoint}?search={search_token}'
        response = self.client.get(url_with_parameters)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_content = response.data
        self.assertEquals(len(response_content), 1)
        self.assertEquals(response_content[0]['id'], user_big_name.id)

    def test_search_user_by_google_drive_exact_value(self):
        baker.make_recipe(
            'user.user_recipe',
            first_name="Ricky",
            last_name="Martin",
            google_drive_spreadsheet_id="00421",

        )
        search_token = "00425"
        url_with_parameters = f'{self.endpoint}?search={search_token}'
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
        search_token = "0042"
        url_with_parameters = f'{self.endpoint}?search={search_token}'

        response = self.client.get(url_with_parameters)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        response_content = response.data
        self.assertEquals(len(response_content), 0)
