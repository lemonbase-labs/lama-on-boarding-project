from rest_framework import status
from django.contrib.auth.hashers import make_password

from review.domain.models.review_cycle import ReviewCycle
from review.tests.ui.base_review_ui_test import BaseReviewUITest
from person.application.services.person_auth import PersonAuthAppService
from review.application.services.review_cycle import ReviewCycleAppService
from person.application.requests.person_register import PersonRegisterRequest
from review.application.requests.review_cylce_create import ReviewCycleCreateRequest


class ReviewCycleViewsetTests(BaseReviewUITest):
    @classmethod
    def setUpTestData(cls):
        cls.person_email = "test2@email.com"
        cls.person2_email = "test3@email.com"
        cls.password = make_password("password")

        cls.person1 = PersonAuthAppService.register(
            PersonRegisterRequest(
                email=cls.person_email,
                password=cls.password,
                name="name_1",
            )
        )
        cls.person2 = PersonAuthAppService.register(
            PersonRegisterRequest(
                email=cls.person2_email,
                password=cls.password,
                name="name_2",
            )
        )

    def setUp(self) -> None:
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

    def test_리뷰_사이클_생성__when__비로그인시__expect__403_forbidden(self):
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

    def test_리뷰_사이클_생성__when__name_필드가_없는_경우__expect__400_bad_request(self):
        self.client.login(email=self.person1.email, password=self.password)
        resp = self.create_review(
            {
                "reviewee_entity_ids": [str(self.person1.entity_id)],
                "question": {
                    "title": "question 1",
                    "description": "description of question 1",
                },
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클_생성__when__reviewee_entity_ids_필드가_없는_경우__expect__400_bad_request(
        self,
    ):
        self.client.login(email=self.person1.email, password=self.password)
        resp = self.create_review(
            {
                "name": "review cycle 1",
                "question": {
                    "title": "question 1",
                    "description": "description of question 1",
                },
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클_생성__when__question_필드가_없는_경우__expect__400_bad_request(self):
        self.client.login(email=self.person1.email, password=self.password)
        resp = self.create_review(
            {
                "name": "review cycle 1",
                "reviewee_entity_ids": [str(self.person1.entity_id)],
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클_생성__when__question_title_필드가_없는_경우__expect__400_bad_request(self):
        self.client.login(email=self.person1.email, password=self.password)
        resp = self.create_review(
            {
                "name": "review cycle 1",
                "reviewee_entity_ids": [str(self.person1.entity_id)],
                "question": {"description": "description of question 1"},
            },
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_리뷰_사이클_생성__when__정상인_경우__expect__201_created(self):
        review_cycle_name = "review cycle 1"
        review_cycle_question_title = "question 1"
        review_Cycle_question_description = "description of question 1"

        self.client.login(email=self.person1.email, password=self.password)
        resp = self.create_review(
            {
                "reviewee_entity_ids": [str(self.person1.entity_id)],
                "name": review_cycle_name,
                "question": {
                    "title": review_cycle_question_title,
                    "description": review_Cycle_question_description,
                },
            },
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        created_review_cycle_entity_id = resp.data["entity_id"]
        review_cycle: ReviewCycle = ReviewCycle.objects.get(
            entity_id=created_review_cycle_entity_id
        )
        self.assertEqual(review_cycle.name, review_cycle_name)
        self.assertEqual(review_cycle.question.title, review_cycle_question_title)
        self.assertEqual(
            review_cycle.question.description, review_Cycle_question_description
        )
        self.assertListEqual(
            [str(reviewee.entity_id) for reviewee in review_cycle.reviewees],
            [str(self.person1.entity_id)],
        )

    def test_리뷰_사이클_업데이트__when__비로그인시__expect__403_forbidden(self):
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

    def test_리뷰_사이클_업데이트__when__생성자가_아닌_경우__expect__403_forbidden(self):
        self.client.login(email=self.person2.email, password=self.password)
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

    def test_리뷰_사이클_업데이트__when__정상인_경우__expect__200_ok(self):
        modified_name = "modified review cycle"
        modified_question_title = "modified question title"
        modified_question_description = "modified question description"

        self.client.login(email=self.person1.email, password=self.password)
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
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.review_cycle.refresh_from_db()

        self.assertEqual(self.review_cycle.name, modified_name)
        self.assertEqual(self.review_cycle.question.title, modified_question_title)
        self.assertEqual(
            self.review_cycle.question.description, modified_question_description
        )

    def test_리뷰_사이클_삭제__when__비로그인시__expect__403_forbidden(self):
        resp = self.delete_review(
            self.review_cycle.entity_id,
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_리뷰_사이클_삭제__when__생성자가_아닌_경우__expect__403_forbidden(self):
        self.client.login(email=self.person2.email, password=self.password)
        resp = self.delete_review(
            self.review_cycle.entity_id,
        )
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_리뷰_사이클_삭제__when__정상인_경우__expect__204_no_content(self):
        self.client.login(email=self.person1.email, password=self.password)
        resp = self.delete_review(
            self.review_cycle.entity_id,
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
