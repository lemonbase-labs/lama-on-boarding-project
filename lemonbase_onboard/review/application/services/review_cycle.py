from common.http_control_exceptions import Unauthorized
from review.application.requests.review_cylce_create import ReviewCycleCreateRequest
from review.domain.services.review_cycle_domain import ReviewCycleDomainService
from review.domain.commands.review_cycle_create import ReviewCycleCreateCommand
from review.domain.commands.review_cycle_update import ReviewCycleUpdateCommand
from review.domain.models.review_cycle import ReviewCycle
from review.application.dtos.review_cycle import ReviewCycleDTO
from person.domain.repositories.person import PersonRepository
from review.domain.services.reviewee_domain import RevieweeDomainService
from review.application.requests.review_cycle_update import ReviewCycleUpdateRequest
from review.domain.commands.reviewee_bulk_update import RevieweeBulkUpdateCommand
from review.domain.commands.reviewee_bulk_create import RevieweeBulkCreateCommand
from review.domain.commands.review_cycle_delete import ReviewCycleDeleteCommand


class ReviewCycleAppService:
    @classmethod
    def create_review_cycle(
        cls, create_review_request: ReviewCycleCreateRequest
    ) -> ReviewCycleDTO:

        review_cycle_create_command = ReviewCycleCreateCommand(
            request_user_id=create_review_request.request_user_id,
            **create_review_request.dict(),
        )
        review_cycle = ReviewCycleDomainService.create_review_cycle(
            review_cycle_create_command=review_cycle_create_command,
        )

        person_list = PersonRepository.find_by_entitiy_ids_exact(
            entity_ids=create_review_request.reviewee_entity_ids
        )
        reviewee_bulk_create_command = RevieweeBulkCreateCommand(
            review_cycle_id=review_cycle.id,
            person_ids=[person.id for person in person_list],
        )
        RevieweeDomainService.create_reviewees(
            reviewee_bulk_create_command=reviewee_bulk_create_command
        )

        return ReviewCycleDTO(review_cycle)

    @classmethod
    def update_review_cycle(
        cls,
        review_cycle_entity_id: str,
        update_review_request: ReviewCycleUpdateRequest,
    ):
        review_cycle_create_command = ReviewCycleUpdateCommand(
            review_cycle_entity_id=review_cycle_entity_id,
            request_user_id=update_review_request.request_user_id,
            **update_review_request.dict(),
        )
        review_cycle = ReviewCycleDomainService.update_review_cycle(
            review_cycle_create_command
        )

        person_list = PersonRepository.find_by_entitiy_ids_exact(
            entity_ids=update_review_request.reviewee_entity_ids
        )
        reviewee_bulk_update_command = RevieweeBulkUpdateCommand(
            review_cycle_id=review_cycle.id,
            person_ids=[person.id for person in person_list],
        )
        RevieweeDomainService.update_reviewees(
            reviewee_bulk_update_command=reviewee_bulk_update_command
        )

        return ReviewCycleDTO(review_cycle)

    @classmethod
    def delete_review_cycle(
        cls, delete_review_cycle_command: ReviewCycleDeleteCommand
    ) -> None:
        ReviewCycleDomainService.delete_review_cycle(delete_review_cycle_command)
