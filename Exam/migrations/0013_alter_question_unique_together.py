# Generated by Django 5.1.3 on 2025-02-13 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Exam", "0012_alter_question_unique_together"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="question",
            unique_together=set(),
        ),
    ]
