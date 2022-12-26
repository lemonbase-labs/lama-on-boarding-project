from typing import List

from pydantic import BaseModel

from person.application.dtos.basic_person import BasicPersonDTO
from review.application.dtos.review_cycle_question import ReviewCycleQuestionDTO


class ReviewCycleDTO(BaseModel):
    id: int
    person: BasicPersonDTO
    name: str
    question: ReviewCycleQuestionDTO
    reviewee: List[BasicPersonDTO]
