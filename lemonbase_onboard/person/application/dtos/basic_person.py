from datetime import datetime

from pydantic import BaseModel


class BasicPersonDTO(BaseModel):
    email: str
    name: str
    registered_at: datetime
