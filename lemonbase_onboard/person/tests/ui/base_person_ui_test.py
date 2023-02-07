from typing import Dict

from rest_framework.test import APIClient, APITestCase
from rest_framework import status


class BasePersonUITest(APITestCase):
    REGISTER_URL = "/person/register/"
    LOGIN_URL = "/person/login/"
    LOGOUT_URL = "/person/logout/"

    def register(self, request_data: Dict):
        return self.client.post(self.REGISTER_URL, request_data)

    def login(self, request_data: Dict):
        return self.client.post(self.LOGIN_URL, request_data)

    def logout(self, request_data: Dict, email: str = None, password: str = None):
        return self.client.post(self.LOGOUT_URL, request_data)