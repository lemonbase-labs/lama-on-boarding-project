from pydantic import EmailStr

from common.base_http_request_model import BaseHttpRequestModel


class PersonLoginRequest(BaseHttpRequestModel):
    username: EmailStr
    password: str
