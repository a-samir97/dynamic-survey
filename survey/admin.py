from django.contrib import admin
from .models import Survey, Section, FieldType, Field, SurveyResponse, FieldResponse

admin.site.register(Survey)
admin.site.register(Section)
admin.site.register(FieldType)
admin.site.register(Field)
admin.site.register(SurveyResponse)
admin.site.register(FieldResponse)
