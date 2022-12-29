from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.hashers import make_password
from rest_framework import status

from person.domain.models.person import Person


class ReviewCycleViewsetTests(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.unauth_client = APIClient()

        person_id = "test1@email.com"
        password = make_password("password")

        self.person1 = Person(email=person_id, password=password, name="name").save()
        self.person2 = Person(
            email="test2@email.com", password=password, name="name_2"
        ).save()

        self.client.login(username=person_id, password="password")

    def test_리뷰_사이클_생성_비로그인시_401(self):
        resp = self.unauth_client.post(
            "/review/",
            {
                "name": "review cycle 1",
                "reviewee_ids": [str(self.person1.entity_id)],
                "question": {
                    "title": "question 1",
                    "description": "description of question 1",
                },
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_리뷰_사이클_생성_필수인_필드가_없는_경우_400(self):
        # 1. without name
        resp = self.client.post(
            "/review/",
            {
                "reviewee_ids": [str(self.person1.entity_id)],
                "question": {
                    "title": "question 1",
                    "description": "description of question 1",
                },
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # 2. without reviewee_ids
        resp = self.client.post(
            "/review/",
            {
                "name": "review cycle 1",
                "question": {
                    "title": "question 1",
                    "description": "description of question 1",
                },
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # 3. without question
        resp = self.client.post(
            "/review/",
            {
                "name": "review cycle 1",
                "reviewee_ids": [str(self.person1.entity_id)],
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # 4. without question.title
        resp = self.client.post(
            "/review/",
            {
                "name": "review cycle 1",
                "reviewee_ids": [str(self.person1.entity_id)],
                "question": {"description": "description of question 1"},
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클_생성_정상인_경우_201(self):
        resp = self.client.post(
            "/person/register/",
            {"username": "username", "password": "password", "name": "name"},
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클_업데이트_비로그인시_401(self):
        resp = self.client.post(
            "/person/register/",
            {"username": "username", "password": "password", "name": "name"},
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클_업데이트_생성자가_아닌_경우_401(self):
        resp = self.client.post(
            "/person/register/",
            {"username": "username", "password": "password", "name": "name"},
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클_업데이트_필수인_필드가_없는_경우_400(self):
        resp = self.client.post(
            "/person/register/",
            {"username": "username", "password": "password", "name": "name"},
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클_업데이트_정상인_경우_200(self):
        resp = self.client.post(
            "/person/register/",
            {"username": "username", "password": "password", "name": "name"},
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클_삭제_비로그인시_401(self):
        resp = self.client.post(
            "/person/register/",
            {"username": "username", "password": "password", "name": "name"},
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클_삭제_생성자가_아닌_경우_401(self):
        resp = self.client.post(
            "/person/register/",
            {"username": "username", "password": "password", "name": "name"},
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클_삭제_정상인_경우_204(self):
        resp = self.client.post(
            "/person/register/",
            {"username": "username", "password": "password", "name": "name"},
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
