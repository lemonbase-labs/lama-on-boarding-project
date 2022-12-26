from common.base_http_request_model import BaseHttpRequestModel


class ReviewCycleCreateQuestionRequest(BaseHttpRequestModel):
    title: str
    description: str
