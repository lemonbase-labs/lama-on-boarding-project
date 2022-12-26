from pydantic import BaseModel, ValidationError

from rest_framework.exceptions import ValidationError as RestValidationError


class BaseHttpRequestModel(BaseModel):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            if (
                key in self.__annotations__.keys()
                and len(value) == 1
                and getattr(self.__annotations__.get(key), "__origin__", None)
                is not list
            ):
                kwargs[key] = value[0]

        try:
            super().__init__(*args, **kwargs)
        except ValidationError as e:
            raise RestValidationError(e)
