# Generated by Django 5.1.3 on 2025-02-10 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Exam", "0004_rename_is_correct_answer_correct_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="exam",
            options={"verbose_name_plural": "Exams"},
        ),
    ]
