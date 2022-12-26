from typing import List

from pydantic import BaseModel

from review.domain.commands.review_cycle_update_question import (
    ReviewCycleUpdateQuestionCommand,
)


class ReviewCycleUpdateCommand(BaseModel):
    review_cycle_id: int
    request_user_id: int
    name: str
    reviewee_ids: List[int]
    question: ReviewCycleUpdateQuestionCommand
