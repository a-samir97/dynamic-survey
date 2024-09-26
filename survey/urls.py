from rest_framework import routers
from .views import (
    SurveyViewSet, SurveyResponseViewSet
)

router = routers.DefaultRouter()
router.register(r"surveys", SurveyViewSet)
router.register(r"survey-responses", SurveyResponseViewSet)

urlpatterns = router.urls
