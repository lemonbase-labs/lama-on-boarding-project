from rest_framework.exceptions import APIException
from rest_framework import status


class HttpForbidden(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "리소스에 접근할 권한이 없습니다"
    default_code = "unauthorized"
