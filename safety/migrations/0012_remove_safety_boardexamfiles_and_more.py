# Generated by Django 5.1.3 on 2025-05-08 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("safety", "0011_alter_safety_educationfiles"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="safety",
            name="boardExamFiles",
        ),
        migrations.RemoveField(
            model_name="safety",
            name="educationFiles",
        ),
        migrations.RemoveField(
            model_name="safety",
            name="notarizedFiles",
        ),
        migrations.RemoveField(
            model_name="safety",
            name="trainingFiles",
        ),
        migrations.RemoveField(
            model_name="safety",
            name="workExperienceFiles",
        ),
        migrations.AddField(
            model_name="safety",
            name="board_exam_file",
            field=models.FileField(
                blank=True, null=True, upload_to="safety/board_exams/"
            ),
        ),
        migrations.AddField(
            model_name="safety",
            name="education_file",
            field=models.FileField(
                blank=True, null=True, upload_to="safety/education/"
            ),
        ),
        migrations.AddField(
            model_name="safety",
            name="notarized_file",
            field=models.FileField(
                blank=True, null=True, upload_to="safety/notarized/"
            ),
        ),
        migrations.AddField(
            model_name="safety",
            name="training_file",
            field=models.FileField(blank=True, null=True, upload_to="safety/training/"),
        ),
        migrations.AddField(
            model_name="safety",
            name="work_experience_file",
            field=models.FileField(
                blank=True, null=True, upload_to="safety/work_experience/"
            ),
        ),
    ]
