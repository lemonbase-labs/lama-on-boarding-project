from typing import List

from common.base_http_request_model import BaseHttpRequestModel
from review.application.requests.review_cycle_create_question import (
    ReviewCycleCreateQuestionRequest,
)


class ReviewCycleUpdateRequest(BaseHttpRequestModel):
    name: str
    reviewee_entity_ids: List[str]
    question: ReviewCycleCreateQuestionRequest
