from rest_framework.viewsets import ModelViewSet
from .models import Survey, SurveyResponse
from .serializers import (
    SurveySerializer, SurveyResponseSerializer
)


class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class SurveyResponseViewSet(ModelViewSet):
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer
