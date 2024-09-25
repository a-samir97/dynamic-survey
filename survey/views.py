from rest_framework.viewsets import ModelViewSet
from .models import Survey, Section, FieldType, Field, SurveyResponse, FieldResponse
from .serializers import (
    SurveySerializer, SectionSerializer, FieldTypeSerializer,
    FieldSerializer, SurveyResponseSerializer, FieldResponseSerializer
)


class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


class SectionViewSet(ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class FieldTypeViewSet(ModelViewSet):
    queryset = FieldType.objects.all()
    serializer_class = FieldTypeSerializer


class FieldViewSet(ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer


class SurveyResponseViewSet(ModelViewSet):
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer


class FieldResponseViewSet(ModelViewSet):
    queryset = FieldResponse.objects.all()
    serializer_class = FieldResponseSerializer
