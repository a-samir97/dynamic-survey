from django.test import TestCase
from survey.models import Survey, Section, FieldType, Field, SurveyResponse


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.survey = Survey.objects.create(
            title='Survey Title',
            description='Survey Description'
        )
        self.section = Section.objects.create(
            survey=self.survey,
            title='Section Title',
            order=1
        )
        self.field_type = FieldType.objects.create(
            name='Text'
        )
        self.field = Field.objects.create(
            section=self.section,
            field_type=self.field_type,
            name='Field Name',
            is_required=True,
            order=1
        )
        self.survey_response = SurveyResponse.objects.create(
            survey=self.survey,
            is_completed=False
        )
        return super().setUp()

    def test_survey_creation(self):
        self.assertEqual(self.survey.title, 'Survey Title')
        self.assertEqual(self.survey.description, 'Survey Description')
        self.assertEqual(self.survey.sections.count(), 1)

    def test_section_creation(self):
        self.assertEqual(self.section.title, 'Section Title')
        self.assertEqual(self.section.order, 1)
        self.assertEqual(self.section.fields.count(), 1)

    def test_field_type_creation(self):
        self.assertEqual(self.field_type.name, 'Text')

    def test_field_creation(self):
        self.assertEqual(self.field.section, self.section)
        self.assertEqual(self.field.field_type, self.field_type)
        self.assertEqual(self.field.name, 'Field Name')
        self.assertTrue(self.field.is_required)
        self.assertEqual(self.field.order, 1)

    def test_survey_response_creation(self):
        self.assertEqual(self.survey_response.survey, self.survey)
        self.assertFalse(self.survey_response.is_completed)
