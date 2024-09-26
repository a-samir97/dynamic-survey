from rest_framework.test import APITestCase
from rest_framework import status
from survey.models import Survey, FieldType, SurveyResponse


class SurveyAPIsTest(APITestCase):
    def setUp(self):
        self.survey = Survey.objects.create(title='Test Survey', description='A test survey')
        self.field_type = FieldType.objects.create(name='text')

    def test_create_survey(self):
        url = '/v1/api/surveys/'
        data = {
            'title': 'New Survey',
            'description': 'A new test survey',
            'sections': [
                {
                    'title': 'New Section',
                    'order': 1,
                    'fields': [
                        {
                            'name': 'New Field',
                            'field_type': self.field_type.id,
                            'is_required': True,
                            'order': 1
                        }
                    ]
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survey.objects.count(), 2)
        self.assertEqual(Survey.objects.last().sections.count(), 1)
        self.assertEqual(Survey.objects.last().sections.first().fields.count(), 1)

    def test_get_surveys(self):
        url = '/v1/api/surveys/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_survey(self):
        url = f'/v1/api/surveys/{self.survey.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.survey.title)

    def test_delete_survey(self):
        url = f'/v1/api/surveys/{self.survey.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Survey.objects.count(), 0)


class SurveyResponseAPIsTest(APITestCase):

    def setUp(self):
        self.survey = Survey.objects.create(title='Test Survey', description='A test survey')
        self.section = self.survey.sections.create(title='Test Section', order=1)
        self.field_type = FieldType.objects.create(name='text')
        self.field = self.section.fields.create(
            name='Test Field', field_type=self.field_type, is_required=True, order=1)

        self.survery_response = self.survey.responses.create()
        self.field_response = self.survery_response.answers.create(
            field=self.field, value='Test Answer'
        )

    def test_create_survey_response(self):
        url = '/v1/api/survey-responses/'
        data = {
            'survey': self.survey.id,
            'answers': [
                {
                    'field': self.field.id,
                    'value': 'Test Answer'
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SurveyResponse.objects.count(), 2)
        self.assertEqual(Survey.objects.last().responses.count(), 2)
        self.assertEqual(Survey.objects.last().responses.first().answers.count(), 1)

    def test_get_survey_responses(self):
        url = '/v1/api/survey-responses/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_survey_response(self):
        url = f'/v1/api/survey-responses/{self.survery_response.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_survey_response(self):
        url = f'/v1/api/survey-responses/{self.survery_response.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SurveyResponse.objects.count(), 0)
