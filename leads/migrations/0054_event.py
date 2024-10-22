# Generated by Django 5.1.1 on 2024-10-22 15:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0053_userprofile_contact_number_userprofile_email_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField(blank=True, null=True)),
                (
                    "organisation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="leads.userprofile",
                    ),
                ),
            ],
        ),
    ]
