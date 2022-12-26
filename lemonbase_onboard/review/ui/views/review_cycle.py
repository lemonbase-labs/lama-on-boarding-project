from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from review.application.requests.review_cycle_delete import ReviewCycleDeleteRequest
from review.application.requests.review_cycle_update import ReviewCycleUpdateRequest
from review.application.requests.review_cylce_create import ReviewCycleCreateRequest
from review.application.services.review_cycle import ReviewCycleAppService


class ReviewCycleViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        review_create_request = ReviewCycleCreateRequest(**request.data)
        review_cycle = ReviewCycleAppService.create_review_cycle(
            create_review_request=review_create_request, request_user_id=request.user.id
        )

        return Response(review_cycle.dict())

    def update(self, request, pk=None):
        review_update_request = ReviewCycleUpdateRequest(**request.data)
        review_cycle = ReviewCycleAppService.update_review_cycle(
            review_cycle_id=pk,
            update_review_request=review_update_request,
            request_user_id=request.user.id,
        )

        return Response(review_cycle.dict())

    def delete(self, request, pk=None):
        review_delete_reqeust = ReviewCycleDeleteRequest(review_cycle_id=pk)
        ReviewCycleAppService.delete_review_cycle(review_delete_reqeust, request_user_id=request.user.id)
