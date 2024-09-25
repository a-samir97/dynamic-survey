from rest_framework import routers
from .views import (
    SurveyViewSet, SectionViewSet, FieldTypeViewSet,
    FieldViewSet, SurveyResponseViewSet, FieldResponseViewSet
)

router = routers.DefaultRouter()
router.register(r"surveys", SurveyViewSet)
router.register(r"sections", SectionViewSet)
router.register(r"field-types", FieldTypeViewSet)
router.register(r"fields", FieldViewSet)
router.register(r"survey-responses", SurveyResponseViewSet)
router.register(r"field-responses", FieldResponseViewSet)

urlpatterns = router.urls
