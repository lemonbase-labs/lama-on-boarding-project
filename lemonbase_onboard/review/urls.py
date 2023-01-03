from rest_framework import routers

from review.ui.views.review_cycle import ReviewCycleViewSet

router = routers.DefaultRouter()
router.register("", ReviewCycleViewSet, basename="review_cycle")

urlpatterns = router.urls
