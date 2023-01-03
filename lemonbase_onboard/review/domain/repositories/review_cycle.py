from common.base_repository import BaseRepository
from review.domain.models.review_cycle import ReviewCycle


class ReviewCycleRepository(BaseRepository):
    model = ReviewCycle
