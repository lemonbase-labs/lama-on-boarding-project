from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.hashers import make_password

from person.domain.models.person import Person
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
        self.person = PersonAuthAppService.register(
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
        expect_user_email = "email@email.com"
        expect_user_name = "name"
        expect_user_password = "password"

        resp = self.register(
            {"email": expect_user_email, "password": expect_user_name, "name": expect_user_password},
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        person = Person.objects.get(email=expect_user_email)
        self.assertEqual(person.email, expect_user_email)
        self.assertEqual(person.name, expect_user_name)
        self.assertEqual(person.password, make_password(expect_user_password))

    def test_로그인__when__없는_계정으로_요청한_경우__expected__401_unauthorized(self):
        resp = self.login(
            {"email": "email@email.com", "password": "password"}
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
        self.client.force_authenticate(email=self.person)
        resp = self.logout()

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
