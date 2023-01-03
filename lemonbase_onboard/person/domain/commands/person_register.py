from pydantic import BaseModel


class PersonRegisterCommand(BaseModel):
    email: str
    password: str
    name: str
