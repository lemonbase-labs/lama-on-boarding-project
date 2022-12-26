from datetime import datetime

from pydantic import BaseModel


class BasicPersonDTO(BaseModel):
    username: str
    name: str
    registered_at: datetime
