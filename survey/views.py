from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Survey, SurveyResponse
from .serializers import (
    SurveySerializer, SurveyResponseSerializer
)
from .services import SurveyService, SurveyResponseService


class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def create(self, request, *args, **kwargs):
        serializer = SurveySerializer(data=request.data)
        survery = SurveyService().create_survey(serializer)
        return Response(SurveySerializer(survery).data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        surveys = SurveyService().get_surveys()
        serializer = SurveySerializer(surveys, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        survey = SurveyService().get_survey(kwargs.get('pk'))
        serializer = SurveySerializer(survey)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        survey_id = kwargs.get('pk')
        SurveyService().delete_survey(survey_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SurveyResponseViewSet(ModelViewSet):
    queryset = SurveyResponse.objects.all()
    serializer_class = SurveyResponseSerializer

    def create(self, request, *args, **kwargs):
        serializer = SurveyResponseSerializer(data=request.data)
        survey_response = SurveyResponseService().create_survey_response(serializer)
        return Response(SurveyResponseSerializer(survey_response).data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        survey_responses = SurveyResponseService().get_survey_responses()
        serializer = SurveyResponseSerializer(survey_responses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        survey_response = SurveyResponseService().get_survey_response(kwargs.get('pk'))
        serializer = SurveyResponseSerializer(survey_response)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        survey_response_id = kwargs.get('pk')
        SurveyResponseService().delete_survey_response(survey_response_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
