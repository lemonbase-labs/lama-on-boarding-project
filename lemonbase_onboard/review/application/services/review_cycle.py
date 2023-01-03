from review.application.requests.review_cylce_create import ReviewCycleCreateRequest
from review.domain.services.review_cycle_domain import ReviewCycleDomainService
from review.domain.commands.review_cycle_create import ReviewCycleCreateCommand
from review.domain.commands.review_cycle_update import ReviewCycleUpdateCommand
from review.domain.models.review_cycle import ReviewCycle
from review.application.dtos.review_cycle import ReviewCycleDTO
from review.application.dtos.review_cycle_question import ReviewCycleQuestionDTO
from person.application.dtos.basic_person import BasicPersonDTO
from person.domain.repositories.person import PersonRepository
from review.domain.services.reviewee_domain import RevieweeDomainService
from review.application.requests.review_cycle_update import ReviewCycleUpdateRequest
from review.domain.commands.reviewee_bulk_update import RevieweeBulkUpdateCommand
from review.domain.commands.reviewee_bulk_create import RevieweeBulkCreateCommand
from review.domain.commands.review_cycle_delete import ReviewCycleDeleteCommand


class ReviewCycleAppService:
    @classmethod
    def _review_cycle_to_dto(cls, review_cycle: ReviewCycle) -> ReviewCycleDTO:
        return ReviewCycleDTO(
            entity_id=str(review_cycle.entity_id),
            name=review_cycle.name,
            person=BasicPersonDTO(
                email=review_cycle.creator.email,
                name=review_cycle.creator.name,
                registered_at=review_cycle.creator.registered_at,
            ),
            question=ReviewCycleQuestionDTO(
                title=review_cycle.question.title,
                description=review_cycle.question.description,
            ),
            reviewee=[
                BasicPersonDTO(
                    email=reviewee.person.email,
                    name=reviewee.person.name,
                    registered_at=reviewee.person.registered_at,
                )
                for reviewee in review_cycle.reviewee_set.all()
            ],
        )

    @classmethod
    def create_review_cycle(
        cls, create_review_request: ReviewCycleCreateRequest
    ) -> ReviewCycleDTO:

        review_cycle_create_command = ReviewCycleCreateCommand(
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

        return cls._review_cycle_to_dto(review_cycle)

    @classmethod
    def update_review_cycle(
        cls,
        review_cycle_entity_id: str,
        update_review_request: ReviewCycleUpdateRequest,
    ):
        review_cycle_create_command = ReviewCycleUpdateCommand(
            review_cycle_entity_id=review_cycle_entity_id,
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

        return cls._review_cycle_to_dto(review_cycle)

    @classmethod
    def delete_review_cycle(
        cls, delete_review_cycle_command: ReviewCycleDeleteCommand
    ) -> None:
        ReviewCycleDomainService.delete_review_cycle(delete_review_cycle_command)
