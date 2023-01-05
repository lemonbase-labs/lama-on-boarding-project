from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.hashers import make_password
from rest_framework import status

from person.domain.models.person import Person
from review.models import ReviewCycle, Reviewee, Question


class ReviewCycleViewsetTests(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.unauth_client = APIClient()

        self.person_id = "test2@email.com"
        self.password = make_password("password")

        self.person2_id = "test3@email.com"

        self.person1 = Person(email=self.person_id, password=self.password, name="name_1")
        self.person2 = Person(
            email=self.person2_id, password=self.password, name="name_2"
        )

        self.person1.save()
        self.person2.save()

        question = Question(title="question 1", description="desc 1")
        question.save()
        self.review_cycle = ReviewCycle(creator=self.person1, name="cycle name1", question=question)
        self.review_cycle.save()
        Reviewee(review_cycle=self.review_cycle, person=self.person1).save()

        self.client.login(username=self.person_id, password="password")

    def test_리뷰_사이클__when__생성_비로그인시__expect__403_forbidden(self):
        resp = self.unauth_client.post(
            "/review/",
            {
                "name": "review cycle 1",
                "reviewee_entity_ids": [str(self.person1.entity_id)],
                "question": {
                    "title": "question 1",
                    "description": "description of question 1",
                },
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_리뷰_사이클__when__생성_필수인_필드가_없는_경우__expect__400_bad_request(self):
        # 1. without name
        resp = self.client.post(
            "/review/",
            {
                "reviewee_entity_ids": [str(self.person1.entity_id)],
                "question": {
                    "title": "question 1",
                    "description": "description of question 1",
                },
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # 2. without reviewee_entity_ids
        resp = self.client.post(
            "/review/",
            {
                "name": "review cycle 1",
                "question": {
                    "title": "question 1",
                    "description": "description of question 1",
                },
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # 3. without question
        resp = self.client.post(
            "/review/",
            {
                "name": "review cycle 1",
                "reviewee_entity_ids": [str(self.person1.entity_id)],
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # 4. without question.title
        resp = self.client.post(
            "/review/",
            {
                "name": "review cycle 1",
                "reviewee_entity_ids": [str(self.person1.entity_id)],
                "question": {"description": "description of question 1"},
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클__when__생성_정상인_경우__expect__201_created(self):
        resp = self.client.post(
            "/review/",
            {
                "reviewee_entity_ids": [str(self.person1.entity_id)],
                "name": "review cycle 1",
                "question": {
                    "title": "question 1",
                    "description": "description of question 1",
                },
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_리뷰_사이클__when__업데이트_비로그인시__expect__403_forbidden(self):
        resp = self.unauth_client.put(
            f"/review/{str(self.review_cycle.entity_id)}/",
            {
                "reviewee_entity_ids": [str(self.person2.entity_id)],
                "name": "modified review cycle",
                "question": {
                    "title": "modified question title",
                    "description": "modified question description",
                },
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_리뷰_사이클__when__업데이트_생성자가_아닌_경우__expect__403_forbidden(self):
        client = APIClient()
        client.login(username=self.person2_id, password="password")

        resp = client.put(
            f"/review/{str(self.review_cycle.entity_id)}/",
            {
                "reviewee_entity_ids": [str(self.person2.entity_id)],
                "name": "modified review cycle",
                "question": {
                    "title": "modified question title",
                    "description": "modified question description",
                },
            },
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_리뷰_사이클__when__업데이트_정상인_경우__expect__200_ok(self):
        modified_name = "modified review cycle"
        modified_question_title = "modified question title"
        modified_question_description = "modified question description"

        resp = self.client.put(
            f"/review/{str(self.review_cycle.entity_id)}/",
            {
                "reviewee_entity_ids": [str(self.person2.entity_id)],
                "name": modified_name,
                "question": {
                    "title": "modified question title",
                    "description": "modified question description",
                },
            },
            format='json',
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.review_cycle.refresh_from_db()

        self.assertEqual(self.review_cycle.name, modified_name)
        self.assertEqual(self.review_cycle.question.title, modified_question_title)
        self.assertEqual(self.review_cycle.question.description, modified_question_description)

    def test_리뷰_사이클__when__삭제_비로그인시__expect__403_forbidden(self):
        resp = self.unauth_client.delete(
            f"/review/{str(self.review_cycle.entity_id)}/",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_리뷰_사이클__when__삭제_생성자가_아닌_경우__expect__403_forbidden(self):
        client = APIClient()
        client.login(username=self.person2_id, password="password")

        resp = client.delete(
            f"/review/{str(self.review_cycle.entity_id)}/",
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_리뷰_사이클__when__삭제_정상인_경우__expect__204_no_content(self):
        resp = self.client.delete(
            f"/review/{str(self.review_cycle.entity_id)}/",
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
