from typing import Dict

from rest_framework.test import APITestCase
from django.urls import reverse


class BaseReviewUITest(APITestCase):
    def create_review(self, request_data: Dict, email: str = None, password: str = None):
        if email and password:
            self.client.login(email=email, password=password)

        return self.client.post(reverse("review_cycle"), request_data, format="json")

    def update_review(self, request_path: str, request_data: Dict, email: str = None, password: str = None):
        if email and password:
            self.client.login(email=email, password=password)

        return self.client.put(reverse("review_cycle", request_path), request_data, format="json")

    def delete_review(self, request_path: str, request_data: Dict, email: str = None, password: str = None):
        if email and password:
            self.client.login(email=email, password=password)

        return self.client.delete(reverse("review_cycle", request_path), request_data, format="json")
