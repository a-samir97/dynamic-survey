from django.test import TestCase
from rest_framework import serializers

from survey.services import SurveyService, SurveyResponseService
from survey.serializers import SurveySerializer, SurveyResponseSerializer
from survey.models import FieldType, Survey


class SurveyServicesTest(TestCase):
    def setUp(self) -> None:
        self.survery_service = SurveyService()
        self.survey = Survey.objects.create(
            title='Survey Title',
            description='Survey Description'
        )

        self.field_type = FieldType.objects.create(
            name='Text'
        )

        return super().setUp()

    def test_create_survey(self):

        survey_data = {
            'title': 'Survey Title',
            'description': 'Survey Description',
            'sections': [
                {
                    'title': 'Section Title',
                    'order': 1,
                    'fields': [
                        {
                            'name': 'Field Name',
                            'is_required': True,
                            'order': 1,
                            'field_type': self.field_type.id
                        }
                    ]
                }
            ]
        }
        survery_serializer = SurveySerializer(data=survey_data)
        survey_serializer = self.survery_service.create_survey(survery_serializer)

        self.assertEqual(survey_serializer.title, 'Survey Title')
        self.assertEqual(survey_serializer.description, 'Survey Description')
        self.assertEqual(survey_serializer.sections.count(), 1)

    def test_delete_survey(self):
        self.survery_service.delete_survey(self.survey.id)
        self.assertEqual(Survey.objects.count(), 0)

    def test_get_survey(self):
        survey = self.survery_service.get_survey(self.survey.id)
        self.assertEqual(survey.title, 'Survey Title')
        self.assertEqual(survey.description, 'Survey Description')
        self.assertEqual(survey.sections.count(), 0)

    def test_get_surveys(self):
        surveys = self.survery_service.get_surveys()
        self.assertEqual(surveys.count(), 1)


class SurveyResponseServicesTest(TestCase):
    def setUp(self) -> None:
        self.survey_response_service = SurveyResponseService()
        self.survey = Survey.objects.create(
            title='Survey Title',
            description='Survey Description'
        )
        self.section = self.survey.sections.create(
            title='Section Title',
            order=1
        )
        self.field_type = FieldType.objects.create(
            name='Text'
        )
        self.field = self.section.fields.create(
            field_type=self.field_type,
            name='Field Name',
            is_required=True,
            order=1
        )
        self.survey_response = self.survey.responses.create(
            is_completed=False
        )
        return super().setUp()

    def test_create_survey_response(self):
        survey_response_data = {
            'survey': self.survey.id,
            'is_completed': False,
            'answers': [
                {
                    'field': 1,
                    'value': 'Test Value'
                }
            ]
        }
        survey_response_serializer = SurveyResponseSerializer(data=survey_response_data)
        survey_response = self.survey_response_service.create_survey_response(survey_response_serializer)

        self.assertEqual(survey_response.survey.title, 'Survey Title')
        self.assertFalse(survey_response.is_completed)
        self.assertEqual(survey_response.answers.count(), 1)

    def test_get_survey_response(self):
        survey_response = self.survey_response_service.get_survey_response(1)
        self.assertEqual(survey_response.survey.title, 'Survey Title')
        self.assertFalse(survey_response.is_completed)

    def test_get_survey_responses(self):
        survey_responses = self.survey_response_service.get_survey_responses()
        self.assertEqual(survey_responses.count(), 1)
    
    def test_validate_conditional_logic_success(self):
        field1 = self.section.fields.create(
            name='Condition Field',
            field_type=self.field_type,
            is_required=True,
            order=1,
            options=['Yes', 'No']
        )

        field2 = self.section.fields.create(
            name='Dependent Field',
            field_type=self.field_type,
            is_required=True,
            order=2,
            conditional_logic={'field_id': field1.id, 'value': 'Yes'}
        )

        # Test when condition is met
        survey_response_data = {
            'survey': self.survey.id,
            'is_completed': False,
            'answers': [
                {'field': field1.id, 'value': 'Yes'},
                {'field': field2.id, 'value': 'Dependent Answer'}
            ]
        }
        survey_response_serializer = SurveyResponseSerializer(data=survey_response_data)
        survey_response = self.survey_response_service.create_survey_response(survey_response_serializer)
        self.assertEqual(survey_response.survey.title, 'Survey Title')
        self.assertFalse(survey_response.is_completed)
        self.assertEqual(survey_response.answers.count(), 2)

    def test_validate_conditional_logic_failure(self):
        field1 = self.section.fields.create(
            name='Condition Field',
            field_type=self.field_type,
            is_required=True,
            order=1,
            options=['Yes', 'No']
        )

        field2 = self.section.fields.create(
            name='Dependent Field',
            field_type=self.field_type,
            is_required=True,
            order=2,
            conditional_logic={'field_id': field1.id, 'value': 'Yes'}
        )

        # Test when condition is unmet
        survey_response_data = {
            'survey': self.survey.id,
            'is_completed': False,
            'answers': [
                {'field': field1.id, 'value': 'No'},
                {'field': field2.id, 'value': 'Dependent Answer'}
            ]
        }
        survey_response_serializer = SurveyResponseSerializer(data=survey_response_data)
        with self.assertRaises(serializers.ValidationError):
            self.survey_response_service.create_survey_response(survey_response_serializer)

    def test_validate_dependencies_success(self):
        field1 = self.section.fields.create(
            name='Parent Field',
            field_type=self.field_type,
            is_required=True,
            order=1,
            options=['Option A', 'Option B']
        )
        field2 = self.section.fields.create(
            name='Child Field',
            field_type=self.field_type,
            is_required=True,
            order=2,
            dependencies=[{'field_id': field1.id, 'value': 'Option A'}]
        )

        survey_response_data = {
            'survey': self.survey.id,
            'is_completed': False,
            'answers': [
                    {'field': field1.id, 'value': 'Option A'},
                    {'field': field2.id, 'value': 'Dependent Answer'}
            ]
        }
        survey_response_serializer = SurveyResponseSerializer(data=survey_response_data)
        survey_response = self.survey_response_service.create_survey_response(survey_response_serializer)
        self.assertEqual(survey_response.survey.title, 'Survey Title')
        self.assertFalse(survey_response.is_completed)
        self.assertEqual(survey_response.answers.count(), 2)

    def test_validate_dependencies_failure(self):
        field1 = self.section.fields.create(
            name='Parent Field',
            field_type=self.field_type,
            is_required=True,
            order=1,
            options=['Option A', 'Option B']
        )
        field2 = self.section.fields.create(
            name='Child Field',
            field_type=self.field_type,
            is_required=True,
            order=2,
            dependencies=[{'field_id': field1.id, 'value': 'Option A'}]
        )

        survey_response_data = {
            'survey': self.survey.id,
            'is_completed': False,
            'answers': [
                    {'field': field1.id, 'value': 'Option B'},
                    {'field': field2.id, 'value': 'Dependent Answer'}
            ]
        }
        survey_response_serializer = SurveyResponseSerializer(data=survey_response_data)
        with self.assertRaises(serializers.ValidationError):
            self.survey_response_service.create_survey_response(survey_response_serializer)
