from pydantic import BaseModel


class ReviewCycleDeleteCommand(BaseModel):
    review_cycle_entity_id: str
    request_user_id: int
