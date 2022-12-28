from pydantic import EmailStr

from common.base_http_request_model import BaseHttpRequestModel


class PersonLoginRequest(BaseHttpRequestModel):
    email: EmailStr
    password: str
