from rest_framework.exceptions import APIException
from rest_framework import status


class Unauthorized(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "리소스에 접근할 권한이 없습니다"
    default_code = "unauthorized"
