from pydantic import EmailStr

from common.base_http_request_model import BaseHttpRequestModel


class PersonRegisterRequest(BaseHttpRequestModel):
    username: EmailStr
    password: str
    name: str
