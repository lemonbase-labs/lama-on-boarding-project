from common.base_repository import BaseRepository
from review.domain.models.reviewee import Reviewee


class RevieweeRepository(BaseRepository):
    model = Reviewee
