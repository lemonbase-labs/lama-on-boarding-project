from pydantic import BaseModel


class ReviewCycleUpdateQuestionCommand(BaseModel):
    title: str
    description: str
