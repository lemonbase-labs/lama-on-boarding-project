from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.hashers import make_password
from rest_framework import status

from person.domain.models.person import Person


class PersonAuthTests(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        Person(
            email="test1@email.com", password=make_password("password"), name="name"
        ).save()

    def test_회원_가입__when__id가_이메일_형식이_아닐_경우__expected__400_bad_request(self):
        resp = self.client.post(
            "/person/register/",
            {"email": "email", "password": "password", "name": "name"},
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_회원_가입__when__id가_이메일_또는_비밀번호_또는_이름이_없는_경우__expected__400_bad_request(self):
        # Case 1. Missing email
        resp = self.client.post(
            "/person/register/", {"password": "password", "name": "name"}
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # Case 2. Missing password
        resp = self.client.post(
            "/person/register/", {"email": "email@email.com", "name": "name"}
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # Case 3. Missing name
        resp = self.client.post(
            "/person/register/",
            {"email": "email@email.com", "password": "password"},
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_회원_가입__when__정상적으로_회원_가입이_됬을_경우__expected__201_created(self):
        resp = self.client.post(
            "/person/register/",
            {"email": "email@email.com", "password": "password", "name": "name"},
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_로그인__when__없는_계정으로_요청한_경우__expected__401_unauthorized(self):
        resp = self.client.post(
            "/person/login/", {"email": "email@email.com", "password": "password"}
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        resp = self.client.post(
            "/person/register/",
            {"email": "email@email.com", "password": "password", "name": "name"},
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_로그인__when__id는_맞지만_비밀번호는_틀린_정보로_요청한_경우__expected__401_unauthorized(self):
        resp = self.client.post(
            "/person/login/",
            {"email": "email@email.com", "password": "password1"},
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_로그인__when__맞는_정보로_요청한_경우__expected__202_accepted(self):
        resp = self.client.post(
            "/person/login/", {"email": "test1@email.com", "password": "password"}
        )
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)

    def test_로그아웃__when__로그인_안한_상태일_경우__expected__403_forbidden(self):
        resp = self.client.post("/person/logout/")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(email="test1@email.com", password="password")
    def test_로그아웃__when__로그인한_상태일_경우__expected__204_no_content(self):
        resp = self.client.post("/person/logout/")

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
