from pydantic import EmailStr

from common.base_http_request_model import BaseHttpRequestModel


class PersonRegisterRequest(BaseHttpRequestModel):
    email: EmailStr
    password: str
    name: str
