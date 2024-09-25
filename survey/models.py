from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Survey(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.title)


class Section(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField()

    def __str__(self) -> str:
        return str(self.title)


class FieldType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.name)


class Field(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='fields')
    field_type = models.ForeignKey(FieldType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_required = models.BooleanField(default=False)
    order = models.PositiveIntegerField()
    options = models.JSONField(default=dict, blank=True)
    conditional_logic = models.JSONField(default=dict, blank=True)
    dependencies = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return str(self.name)


class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    # user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name='survey_responses')
    completed_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    current_step = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.survey.title)


class FieldResponse(models.Model):
    survey_response = models.ForeignKey(
        SurveyResponse, on_delete=models.CASCADE, related_name='field_responses')
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    value = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.field.name)
