# Generated by Django 5.1.1 on 2024-09-26 05:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("survey", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fieldresponse",
            name="survey_response",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="answers",
                to="survey.surveyresponse",
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="survey",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sections",
                to="survey.survey",
            ),
        ),
    ]
