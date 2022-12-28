from rest_framework.exceptions import APIException


class Unauthorized(APIException):
    status_code = 401
    default_detail = "리소스에 접근할 권한이 없습니다"
    default_code = "unauthorized"
