from typing import List

from pydantic import BaseModel

from review.domain.commands.review_cycle_create_question import (
    ReviewCycleCreateQuestionCommand,
)


class ReviewCycleCreateCommand(BaseModel):
    request_user_id: int
    name: str
    question: ReviewCycleCreateQuestionCommand
