from rest_framework import serializers
from .models import Survey, Section, Field, SurveyResponse, FieldResponse


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        exclude = ['section']


class SectionSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)

    class Meta:
        model = Section
        fields = ['id', 'title', 'order', 'fields']


class SurveySerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True)

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'sections', 'created_at', 'updated_at']


class FieldResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldResponse
        exclude = ['survey_response']


class SurveyResponseSerializer(serializers.ModelSerializer):
    answers = FieldResponseSerializer(many=True)

    class Meta:
        model = SurveyResponse
        fields = ['id', 'survey', 'completed_at', 'is_completed', 'current_step', 'answers', 'created_at', 'updated_at']
