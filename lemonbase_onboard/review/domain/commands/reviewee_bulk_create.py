from typing import List

from pydantic import BaseModel


class RevieweeBulkCreateCommand(BaseModel):
    review_cycle_id: int
    person_ids: List[int]