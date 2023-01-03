from pydantic import BaseModel, ValidationError

from rest_framework.exceptions import ValidationError as RestValidationError


class BaseHttpRequestModel(BaseModel):
    def _check_non_list_type(self, key, value) -> bool:
        """
        GET method 의 parameter 혹은 그 외 method들의 data 중 form-data 인 경우
        기본 field=[value] 형태로 들어오는 데이터를 field=value 형태로 바꿔주기 위해 판단하는 함수

        :return: bool
        """
        return (key in self.__annotations__.keys()
                and len(value) == 1
                and getattr(self.__annotations__.get(key), "__origin__", None)
                is not list)

    def __init__(self, *args, **kwargs):
        kwargs = self._convert(kwargs)
        for key, value in kwargs.items():
            if self._check_non_list_type(key, value):
                kwargs[key] = value[0]

        try:
            super().__init__(*args, **kwargs)
        except ValidationError as e:
            raise RestValidationError(e)
