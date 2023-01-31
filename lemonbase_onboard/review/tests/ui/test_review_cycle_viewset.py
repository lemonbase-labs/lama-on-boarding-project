from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.hashers import make_password

from review.tests.ui.base_review_ui_test import BaseReviewUITest
from person.application.services.person_auth import PersonAuthAppService
from review.application.services.review_cycle import ReviewCycleAppService
from person.application.requests.person_register import PersonRegisterRequest
from review.application.requests.review_cylce_create import ReviewCycleCreateRequest


class ReviewCycleViewsetTests(BaseReviewUITest):
    @classmethod
    def setUpTestData(cls):
        cls.person_id = "test2@email.com"
        cls.password = make_password("password")

        cls.person2_id = "test3@email.com"

    def setUp(self) -> None:
        self.client = APIClient()
        self.person1 = PersonAuthAppService.register(
            PersonRegisterRequest(
                email=self.person_id,
                password=self.password,
                name="name_1",
            )
        )
        self.person2 = PersonAuthAppService.register(
            PersonRegisterRequest(
                email=self.person2_id,
                password=self.password,
                name="name_2",
            )
        )

        self.review_cycle = ReviewCycleAppService.create_review_cycle(
            ReviewCycleCreateRequest(
                name="cycle name1",
                reviewee_entity_ids=[self.person1.entity_id],
                question={
                    "title": "question 1",
                    "description": "desc 1",
                },
                request_user_id=self.person1.entity_id,
            )
        )

    def test_리뷰_사이클__when__생성_비로그인시__expect__403_forbidden(self):
        resp = self.create_review(
            {
                "name": "review cycle 1",
                "reviewee_entity_ids": [str(self.person1.entity_id)],
                "question": {
                    "title": "question 1",
                    "description": "description of question 1",
                },
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_리뷰_사이클__when__생성시_name_필드가_없는_경우__expect__400_bad_request(self):
        resp = self.create_review(
            {
                "reviewee_entity_ids": [str(self.person1.entity_id)],
                "question": {
                    "title": "question 1",
                    "description": "description of question 1",
                },
            },
            email=self.person1.email,
            password=self.password,
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클__when__생성시_reviewee_entity_ids_필드가_없는_경우__expect__400_bad_request(self):
        resp = self.create_review(
            {
                "name": "review cycle 1",
                "question": {
                    "title": "question 1",
                    "description": "description of question 1",
                },
            },
            email=self.person1.email,
            password=self.password,
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클__when__생성시_question_필드가_없는_경우__expect__400_bad_request(self):
        resp = self.create_review(
            {
                "name": "review cycle 1",
                "reviewee_entity_ids": [str(self.person1.entity_id)],
            },
            email=self.person1.email,
            password=self.password,
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클__when__생성시_question_title_필드가_없는_경우__expect__400_bad_request(self):
        resp = self.create_review(
            {
                "name": "review cycle 1",
                "reviewee_entity_ids": [str(self.person1.entity_id)],
                "question": {"description": "description of question 1"},
            },
            email=self.person1.email,
            password=self.password,
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클__when__생성_정상인_경우__expect__201_created(self):
        resp = self.create_review(
            {
                "reviewee_entity_ids": [str(self.person1.entity_id)],
                "name": "review cycle 1",
                "question": {
                    "title": "question 1",
                    "description": "description of question 1",
                },
            },
            email=self.person1.email,
            password=self.password,
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_리뷰_사이클__when__업데이트_비로그인시__expect__403_forbidden(self):
        resp = self.update_review(
            self.review_cycle.entity_id,
            {
                "reviewee_entity_ids": [str(self.person2.entity_id)],
                "name": "modified review cycle",
                "question": {
                    "title": "modified question title",
                    "description": "modified question description",
                },
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_리뷰_사이클__when__업데이트_생성자가_아닌_경우__expect__403_forbidden(self):
        resp = self.update_review(
            self.review_cycle.entity_id,
            {
                "reviewee_entity_ids": [str(self.person2.entity_id)],
                "name": "modified review cycle",
                "question": {
                    "title": "modified question title",
                    "description": "modified question description",
                },
            },
            email=self.person2.email,
            password=self.password,
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_리뷰_사이클__when__업데이트_정상인_경우__expect__200_ok(self):
        modified_name = "modified review cycle"
        modified_question_title = "modified question title"
        modified_question_description = "modified question description"

        resp = self.update_review(
            self.review_cycle.entity_id,
            {
                "reviewee_entity_ids": [str(self.person2.entity_id)],
                "name": modified_name,
                "question": {
                    "title": "modified question title",
                    "description": "modified question description",
                },
            },
            email=self.person1.email,
            password=self.password,
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.review_cycle.refresh_from_db()

        self.assertEqual(self.review_cycle.name, modified_name)
        self.assertEqual(self.review_cycle.question.title, modified_question_title)
        self.assertEqual(self.review_cycle.question.description, modified_question_description)

    def test_리뷰_사이클__when__삭제_비로그인시__expect__403_forbidden(self):
        resp = self.delete_review(
            self.review_cycle.entity_id,
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_리뷰_사이클__when__삭제_생성자가_아닌_경우__expect__403_forbidden(self):
        resp = self.delete_review(
            self.review_cycle.entity_id,
            email=self.person2.email,
            password=self.password,
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_리뷰_사이클__when__삭제_정상인_경우__expect__204_no_content(self):
        resp = self.delete_review(
            self.review_cycle.entity_id,
            email=self.person1.email,
            password=self.password,
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
