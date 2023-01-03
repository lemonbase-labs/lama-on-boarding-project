from pydantic import BaseModel


class ReviewCycleCreateQuestionCommand(BaseModel):
    title: str
    description: str
