from pydantic import BaseModel


class PersonRegisterCommand(BaseModel):
    username: str
    password: str
    name: str
