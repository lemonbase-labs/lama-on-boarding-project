from typing import List

from pydantic import BaseModel

from review.domain.commands.review_cycle_update_question import (
    ReviewCycleUpdateQuestionCommand,
)


class ReviewCycleUpdateCommand(BaseModel):
    review_cycle_entity_id: str
    request_user_id: int
    name: str
    reviewee_entity_ids: List[str]
    question: ReviewCycleUpdateQuestionCommand
