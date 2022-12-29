from common.http_control_exceptions import Unauthorized
from review.application.requests.review_cylce_create import ReviewCycleCreateRequest
from review.application.requests.review_cycle_delete import ReviewCycleDeleteRequest
from review.domain.services.review_cycle_domain import ReviewCycleDomainService
from review.domain.commands.review_cycle_create import ReviewCycleCreateCommand
from review.domain.commands.review_cycle_update import ReviewCycleUpdateCommand
from review.domain.models.review_cycle import ReviewCycle
from review.application.dtos.review_cycle import ReviewCycleDTO
from review.application.dtos.review_cycle_question import ReviewCycleQuestionDTO
from person.application.dtos.basic_person import BasicPersonDTO
from review.domain.repositories.review_cycle import ReviewCycleRepository
from review.application.requests.review_cycle_update import ReviewCycleUpdateRequest


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
        cls, create_review_request: ReviewCycleCreateRequest, request_user_id: int
    ) -> ReviewCycleDTO:
        review_cycle_create_command = ReviewCycleCreateCommand(
            request_user_id=request_user_id,
            **create_review_request.dict(),
        )
        review_cycle = ReviewCycleDomainService.create_review_cycle(
            review_cycle_create_command=review_cycle_create_command,
        )

        return cls._review_cycle_to_dto(review_cycle)

    @classmethod
    def update_review_cycle(
        cls,
        review_cycle_entity_id: str,
        update_review_request: ReviewCycleUpdateRequest,
        request_user_id: int,
    ):
        review_cycle_create_command = ReviewCycleUpdateCommand(
            review_cycle_entity_id=review_cycle_entity_id,
            request_user_id=request_user_id,
            **update_review_request.dict(),
        )
        review_cycle = ReviewCycleDomainService.update_review_cycle(
            review_cycle_create_command
        )

        return cls._review_cycle_to_dto(review_cycle)

    @classmethod
    def delete_review_cycle(
        cls, delete_review_request: ReviewCycleDeleteRequest, request_user_id: int
    ) -> None:
        review_cycle: ReviewCycle = ReviewCycleRepository.find_one(
            entity_id=delete_review_request.review_cycle_entity_id
        )
        if review_cycle.creator.id != request_user_id:
            raise Unauthorized("리뷰 사이클 생성자만 삭제가 가능합니다")

        review_cycle.delete()
