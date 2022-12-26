from common.base_repository import BaseRepository
from review.domain.models.review_cycle import ReviewCycle
from review.domain.repositories.review_cycle_builder import ReviewCycleBuilder


class ReviewCycleRepository(BaseRepository):
    model = ReviewCycle
    builder = ReviewCycleBuilder
