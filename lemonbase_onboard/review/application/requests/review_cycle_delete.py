from common.base_http_request_model import BaseHttpRequestModel


class ReviewCycleDeleteRequest(BaseHttpRequestModel):
    review_cycle_id: int
