from typing import List

from review.domain.models.reviewee import Reviewee
from review.domain.commands.reviewee_bulk_create import RevieweeBulkCreateCommand
from review.domain.commands.reviewee_bulk_update import RevieweeBulkUpdateCommand
from review.domain.repositories.reviewee import RevieweeRepository


class RevieweeDomainService:
    @classmethod
    def create_reviewees(
        cls, reviewee_bulk_create_command: RevieweeBulkCreateCommand
    ) -> List[Reviewee]:
        return cls._create_reviewees(
            reviewee_bulk_create_command.review_cycle_id,
            reviewee_bulk_create_command.person_ids,
        )

    @classmethod
    def _create_reviewees(cls, review_cycle_id: int, person_ids: List[int]):
        created_reviewee: List[Reviewee] = []
        for reviewee_person_id in person_ids:
            created_reviewee.append(
                Reviewee(
                    person_id=reviewee_person_id,
                    review_cycle_id=review_cycle_id,
                )
            )

        return Reviewee.objects.bulk_create(created_reviewee)

    @classmethod
    def _is_changed_reviewee_set(
        cls, origin_reviewee: List[Reviewee], reviewee_ids: List[int]
    ) -> bool:
        # TODO: 순서가 중요한지에 따라, 순서 체크시 로직을 추가한다
        origin_reviewee_person_ids = set(
            [reviewee.person_id for reviewee in origin_reviewee]
        )
        request_reviewee_person_ids = set(reviewee_ids)

        return origin_reviewee_person_ids != request_reviewee_person_ids

    @classmethod
    def _reset_reviewees(cls, review_cycle_id: int, reviewee_ids: List[int]):
        RevieweeRepository.find(review_cycle_id=review_cycle_id).delete()
        cls._create_reviewees(review_cycle_id, reviewee_ids)

    @classmethod
    def update_reviewees(
        cls, reviewee_bulk_update_command: RevieweeBulkUpdateCommand
    ) -> List[Reviewee]:
        before_reviewees: List[Reviewee] = RevieweeRepository.find(
            review_cycle_id=reviewee_bulk_update_command.review_cycle_id
        )
        if cls._is_changed_reviewee_set(
            before_reviewees, reviewee_bulk_update_command.person_ids
        ):
            cls._reset_reviewees(
                reviewee_bulk_update_command.review_cycle_id,
                reviewee_bulk_update_command.person_ids,
            )
