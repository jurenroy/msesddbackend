# Generated by Django 5.1.3 on 2025-05-13 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("safety", "0017_remove_safety_application_form_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="safety",
            name="application_form",
            field=models.FileField(
                blank=True, null=True, upload_to="application_forms/"
            ),
        ),
        migrations.AddField(
            model_name="safety",
            name="notarized_document",
            field=models.FileField(blank=True, null=True, upload_to="notarized_docs/"),
        ),
        migrations.AddField(
            model_name="safety",
            name="photo",
            field=models.FileField(blank=True, null=True, upload_to="photos/"),
        ),
        migrations.AddField(
            model_name="safety",
            name="proof_document",
            field=models.FileField(blank=True, null=True, upload_to="proof_docs/"),
        ),
    ]
