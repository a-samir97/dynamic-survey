from django.test import TestCase
from survey.models import Survey, FieldType, Field
from survey.serializers import SurveySerializer, SectionSerializer, FieldSerializer, SurveyResponseSerializer


class SerializerTests(TestCase):
    def setUp(self) -> None:
        self.field_type = FieldType.objects.create(
            name='Text'
        )
        self.survey = Survey.objects.create(
            title='Survey Title',
            description='Survey Description'
        )
        self.section = self.survey.sections.create(
            title='Section Title',
            order=1
        )
        self.field = Field.objects.create(
            section=self.section,
            field_type=self.field_type,
            name='Field Name',
            is_required=True,
            order=1
        )

        return super().setUp()

    def test_survey_serializer(self):
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
        serializer = SurveySerializer(data=survey_data)

        self.assertTrue(serializer.is_valid(raise_exception=True))
        # survey = serializer.save()
        # self.assertEqual(survey.title, 'Survey Title')
        # self.assertEqual(survey.description, 'Survey Description')
        # self.assertEqual(survey.sections.count(), 1)

    def test_section_serializer(self):
        section_data = {
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
        serializer = SectionSerializer(data=section_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_field_serializer(self):
        field_data = {
            'name': 'Field Name',
            'is_required': True,
            'order': 1,
            'field_type': self.field_type.id
        }
        serializer = FieldSerializer(data=field_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_survey_response_serializer(self):
        survey_response_data = {
            'survey': self.survey.id,
            'is_completed': False,
            'answers': [
                {
                    'field': self.field.id,
                    'value': 'Field Value'
                }
            ]
        }
        serializer = SurveyResponseSerializer(data=survey_response_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
