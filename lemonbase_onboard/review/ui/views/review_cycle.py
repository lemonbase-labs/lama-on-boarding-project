from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from review.application.requests.review_cycle_update import ReviewCycleUpdateRequest
from review.application.requests.review_cylce_create import ReviewCycleCreateRequest
from review.application.services.review_cycle import ReviewCycleAppService
from review.domain.commands.review_cycle_delete import ReviewCycleDeleteCommand


class ReviewCycleViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        review_create_request = ReviewCycleCreateRequest(
            **request.data, request_user_id=request.user.id
        )
        review_cycle = ReviewCycleAppService.create_review_cycle(
            create_review_request=review_create_request,
        )

        return Response(review_cycle.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        review_update_request = ReviewCycleUpdateRequest(
            **request.data, request_user_id=request.user.id
        )
        review_cycle = ReviewCycleAppService.update_review_cycle(
            review_cycle_entity_id=pk,
            update_review_request=review_update_request,
        )

        return Response(review_cycle.data)

    def delete(self, request, pk=None):
        review_delete_reqeust = ReviewCycleDeleteCommand(
            review_cycle_entity_id=pk, request_user_id=request.user.id
        )
        ReviewCycleAppService.delete_review_cycle(review_delete_reqeust)

        return Response(None, status=status.HTTP_204_NO_CONTENT)
