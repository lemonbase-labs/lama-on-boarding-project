from typing import List

from pydantic import BaseModel

from person.application.dtos.basic_person import BasicPersonDTO
from review.application.dtos.review_cycle_question import ReviewCycleQuestionDTO


class ReviewCycleDTO(BaseModel):
    entity_id: str
    person: BasicPersonDTO
    name: str
    question: ReviewCycleQuestionDTO
    reviewee: List[BasicPersonDTO]
