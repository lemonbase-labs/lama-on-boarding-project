from typing import Dict

from django.urls import reverse
from rest_framework.test import APIClient, APITestCase


class BaseReviewUITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

    def create_review(self, request_data: Dict):
        return self.client.post(reverse("review_cycle"), request_data, format="json")

    def update_review(self, request_path: str, request_data: Dict):
        return self.client.put(reverse("review_cycle", request_path), request_data, format="json")

    def delete_review(self, request_path: str, request_data: Dict):
        return self.client.delete(reverse("review_cycle", request_path), request_data, format="json")
