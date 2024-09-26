from typing import List

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from survey.models import Survey, SurveyResponse
from survey.serializers import SurveySerializer, SurveyResponseSerializer


class SurveyService:
    def get_survey(self, survey_id: int) -> Survey:
        survey = get_object_or_404(Survey, id=survey_id)
        return survey

    def get_surveys(self) -> List[Survey]:
        surverys = Survey.objects.all()
        return surverys

    @transaction.atomic
    def create_survey(self, survey_serializer: SurveySerializer) -> Survey:
        survey_serializer.is_valid(raise_exception=True)
        sections_data = survey_serializer.validated_data.pop('sections')
        survey = Survey.objects.create(**survey_serializer.validated_data)
        for section_data in sections_data:
            fields_data = section_data.pop('fields')
            section = survey.sections.create(**section_data)
            for field_data in fields_data:
                section.fields.create(**field_data)
        return survey

    def delete_survey(self, survey_id: int) -> None:
        survey = self.get_survey(survey_id)
        survey.delete()


class SurveyResponseService:

    def get_survey_response(self, survey_response_id: int) -> SurveyResponse:
        survey_response = get_object_or_404(SurveyResponse, id=survey_response_id)
        return survey_response

    def get_survey_responses(self) -> List[SurveyResponse]:
        survey_responses = SurveyResponse.objects.all()
        return survey_responses

    @transaction.atomic
    def create_survey_response(
            self, survey_response_serializer: SurveyResponseSerializer) -> SurveyResponse:
        survey_response_serializer.is_valid(raise_exception=True)

        answers_data = survey_response_serializer.validated_data.pop('answers')
        # Validate conditional logic
        self._validate_conditional_logic(survey_response_serializer.validated_data, answers_data)
        # Validate dependencies
        self._validate_dependencies(survey_response_serializer.validated_data, answers_data)

        survey_response = SurveyResponse.objects.create(**survey_response_serializer.validated_data)
        for answer_data in answers_data:
            survey_response.answers.create(**answer_data)
        return survey_response

    def _validate_conditional_logic(self, survery_response_data: dict, answers: dict):
        survery = survery_response_data['survey']
        sections = survery.sections.all()

        for section in sections:
            for field in section.fields.all():

                if field.conditional_logic:
                    condition_met = self._evalute_condition(field.conditional_logic, answers)
                    if not condition_met:
                        raise serializers.ValidationError(
                            f"Conditional logic failed for field {field.name}"
                        )

    def _evalute_condition(self, condition: dict, answers: dict) -> bool:
        field = condition['field_id']
        expected_value = condition['value']
        answer = answers.get(field)

        return answer and answer == expected_value

    def _validate_dependencies(self, survery_response_data: dict, answers: dict):
        survery = survery_response_data['survey']
        sections = survery.sections.all()

        for section in sections:
            for field in section.fields.all():
                if field.dependencies:
                    for dependency in field.dependencies:
                        dependent_field = dependency['field_id']
                        dependent_value = dependency['value']
                        dependent_answer = answers.get(dependent_field)
                        if dependent_answer != dependent_value:
                            raise serializers.ValidationError(
                                f"Dependency failed for field {field.name}"
                            )

    def delete_survey_response(self, survey_response_id: int) -> None:
        survey_response = self.get_survey_response(survey_response_id)
        survey_response.delete()
