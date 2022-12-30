from typing import List

from django.db import transaction

from common.http_control_exceptions import Unauthorized
from review.domain.models.review_cycle import ReviewCycle
from review.domain.models.question import Question
from review.domain.models.reviewee import Reviewee
from review.domain.commands.review_cycle_create import ReviewCycleCreateCommand
from review.domain.commands.review_cycle_update import ReviewCycleUpdateCommand
from review.domain.repositories.review_cycle import ReviewCycleRepository
from review.domain.commands.review_cycle_create_question import (
    ReviewCycleCreateQuestionCommand,
)
from review.domain.commands.review_cycle_update_question import (
    ReviewCycleUpdateQuestionCommand,
)


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

        cls._create_reviewees(review_cycle, review_cycle_create_command.reviewee_ids)

        return review_cycle

    @classmethod
    def _reset_reviewees(cls, review_cycle: ReviewCycle, reviewee_ids: List[int]):
        review_cycle.reviewee_set.all().delete()
        cls._create_reviewees(review_cycle, reviewee_ids)

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
    @transaction.atomic
    def update_review_cycle(
        cls, review_cycle_update_command: ReviewCycleUpdateCommand
    ) -> ReviewCycle:
        review_cycle: ReviewCycle = ReviewCycleRepository.find_one(
            entity_id=review_cycle_update_command.review_cycle_entity_id
        )

        if review_cycle.creator.id != review_cycle_update_command.request_user_id:
            raise Unauthorized("리뷰 사이클 생성자만 업데이트를 할 수 있습니다")

        review_cycle.name = review_cycle_update_command.name

        cls._update_question(
            review_cycle.question, review_cycle_update_command.question
        )

        return review_cycle
