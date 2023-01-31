from typing import Dict

from rest_framework.test import APIClient, APITestCase
from rest_framework import status

from person.tests.ui.base_person_ui_test import BasePersonUITest
from person.application.services.person_auth import PersonAuthAppService
from person.application.requests.person_register import PersonRegisterRequest


class PersonAuthTests(BasePersonUITest):
    @classmethod
    def setUpTestData(cls):
        cls.person_email = "test1@email.com"
        cls.person_password = "password"

    def setUp(self) -> None:
        self.client = APIClient()
        PersonAuthAppService.register(
            PersonRegisterRequest(
                email=self.person_email, password=self.person_password, name="name"
            )
        )

    def test_회원_가입__when__id가_이메일_형식이_아닐_경우__expected__400_bad_request(self):
        resp = self.register({"email": "email", "password": "password", "name": "name"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_회원_가입__when__id가_이메일이_없는_경우__expected__400_bad_request(self):
        resp = self.register({"password": "password", "name": "name"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_회원_가입__when__id가_비밀번호가_없는_경우__expected__400_bad_request(self):
        resp = self.register({"email": "email@email.com", "name": "name"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_회원_가입__when__id가_이름이_없는_경우__expected__400_bad_request(self):
        resp = self.register(
            {"email": "email@email.com", "password": "password"},
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_회원_가입__when__정상적으로_회원_가입이_됬을_경우__expected__201_created(self):
        resp = self.register(
            {"email": "email@email.com", "password": "password", "name": "name"},
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_로그인__when__없는_계정으로_요청한_경우__expected__401_unauthorized(self):
        resp = self.login(
            "/person/login/", {"email": "email@email.com", "password": "password"}
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_로그인__when__id는_맞지만_비밀번호는_틀린_정보로_요청한_경우__expected__401_unauthorized(self):
        wrong_password = "wrong_password"
        resp = self.login(
            {"email": self.person_email, "password": wrong_password},
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_로그인__when__맞는_정보로_요청한_경우__expected__202_accepted(self):
        resp = self.login(
            {"email": "test1@email.com", "password": "password"}
        )
        self.assertEqual(resp.status_code, status.HTTP_202_ACCEPTED)

    def test_로그아웃__when__로그인_안한_상태일_경우__expected__403_forbidden(self):
        resp = self.logout()
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_로그아웃__when__로그인한_상태일_경우__expected__204_no_content(self):
        resp = self.logout(email=self.person_email, password=self.person_password)

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
