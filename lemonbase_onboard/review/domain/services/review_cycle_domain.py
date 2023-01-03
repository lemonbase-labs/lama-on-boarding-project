from django.db import transaction

from common.http_control_exceptions import HttpForbidden
from review.domain.models.review_cycle import ReviewCycle
from review.domain.models.question import Question
from review.domain.commands.review_cycle_create import ReviewCycleCreateCommand
from review.domain.commands.review_cycle_update import ReviewCycleUpdateCommand
from review.domain.repositories.review_cycle import ReviewCycleRepository
from review.domain.commands.review_cycle_create_question import (
    ReviewCycleCreateQuestionCommand,
)
from review.domain.commands.review_cycle_update_question import (
    ReviewCycleUpdateQuestionCommand,
)
from review.domain.commands.review_cycle_delete import ReviewCycleDeleteCommand


class ReviewCycleDomainService:
    @classmethod
    def _create_question(
        cls, question_create_command: ReviewCycleCreateQuestionCommand
    ) -> Question:
        question = Question(
            title=question_create_command.title,
            description=question_create_command.description,
        )
        question.save()

        return question

    @classmethod
    @transaction.atomic
    def create_review_cycle(
        cls, review_cycle_create_command: ReviewCycleCreateCommand
    ) -> ReviewCycle:
        question = cls._create_question(review_cycle_create_command.question)

        review_cycle = ReviewCycle(
            creator_id=review_cycle_create_command.request_user_id,
            name=review_cycle_create_command.name,
            question=question,
        )
        review_cycle.save()

        return review_cycle

    @classmethod
    def _update_question(
        cls,
        question: Question,
        update_question_command: ReviewCycleUpdateQuestionCommand,
    ) -> Question:
        question.title = update_question_command.title
        question.description = update_question_command.description

        question.save()

    @classmethod
    def _check_review_cycle_permission(
        cls, review_cycle: ReviewCycle, request_person_id: int
    ):
        if review_cycle.creator.id != request_person_id:
            raise HttpForbidden("리뷰 사이클 생성자만 해당 액션을 할 수 있습니다")

    @classmethod
    @transaction.atomic
    def update_review_cycle(
        cls, review_cycle_update_command: ReviewCycleUpdateCommand
    ) -> ReviewCycle:
        review_cycle: ReviewCycle = ReviewCycleRepository.find_one(
            entity_id=review_cycle_update_command.review_cycle_entity_id
        )

        cls._check_review_cycle_permission(
            review_cycle, review_cycle_update_command.request_user_id
        )

        review_cycle.name = review_cycle_update_command.name

        cls._update_question(
            review_cycle.question, review_cycle_update_command.question
        )
        review_cycle.save()

        return review_cycle

    @classmethod
    def delete_review_cycle(cls, delete_review_command: ReviewCycleDeleteCommand):
        review_cycle: ReviewCycle = ReviewCycleRepository.find_one(
            entity_id=delete_review_command.review_cycle_entity_id
        )
        cls._check_review_cycle_permission(
            review_cycle, delete_review_command.request_user_id
        )

        review_cycle.delete()
