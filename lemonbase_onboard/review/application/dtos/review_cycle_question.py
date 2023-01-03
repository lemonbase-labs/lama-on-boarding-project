from pydantic import BaseModel


class ReviewCycleQuestionDTO(BaseModel):
    title: str
    description: str
