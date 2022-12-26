from common.base_http_request_model import BaseHttpRequestModel


class ReviewCycleUpdateQuestionRequest(BaseHttpRequestModel):
    title: str
    description: str
