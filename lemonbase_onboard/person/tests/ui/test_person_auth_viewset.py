from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.hashers import make_password
from rest_framework import status

from person.domain.models.person import Person


class PersonAuthTests(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        Person(
            username="test1@email.com", password=make_password("password"), name="name"
        ).save()

    def test_회원_가입시_id가_이메일_형식이_아닐_경우_400(self):
        resp = self.client.post(
            "/person/register/",
            {"username": "username", "password": "password", "name": "name"},
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_회원_가입시_id가_이메일_또는_비밀번호_또는_이름이_없는_경우_400(self):
        client = APIClient()

        # Case 1. Missing username
        resp = self.client.post(
            "/person/register/", {"password": "password", "name": "name"}
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # Case 2. Missing password
        resp = self.client.post(
            "/person/register/", {"username": "username@email.com", "name": "name"}
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # Case 3. Missing name
        resp = self.client.post(
            "/person/register/",
            {"username": "username@email.com", "password": "password"},
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_회원_가입시_정상적으로_회원_가입이_됬을_경우_201(self):
        resp = self.client.post(
            "/person/register/",
            {"username": "username@email.com", "password": "password", "name": "name"},
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_로그인시_없는_계정으로_요청한_경우_401(self):
        resp = self.client.post(
            "/person/login/", {"username": "username@email.com", "password": "password"}
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_로그인시_id는_맞지만_비밀번호는_틀린_정보로_요청한_경우_401(self):
        resp = self.client.post(
            "/person/register/",
            {"username": "username@email.com", "password": "password", "name": "name"},
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        resp = self.client.post(
            "/person/login/",
            {"username": "username@email.com", "password": "password1"},
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_로그인시_맞는_정보로_요청한_경우_202(self):
        resp = self.client.post(
            "/person/login/", {"username": "test1@email.com", "password": "password"}
        )
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)

    def test_로그아웃시_로그인_안한_상태일_경우_401(self):
        resp = self.client.post("/person/logout/")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_로그아웃시_로그인한_상태일_경우_204(self):
        self.client.login(username="test1@email.com", password="password")
        resp = self.client.post("/person/logout/")

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
