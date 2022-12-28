from rest_framework import routers

from person.ui.views.person_auth import PersonAuthViewSet

router = routers.DefaultRouter()
router.register("", PersonAuthViewSet, basename="user")

urlpatterns = router.urls
