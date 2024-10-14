# Generated by Django 5.1.1 on 2024-10-14 11:57

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0005_emiplan"),
    ]

    operations = [
        migrations.CreateModel(
            name="Daybook",
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
                ("date", models.DateField(default=django.utils.timezone.now)),
                (
                    "activity",
                    models.CharField(
                        choices=[
                            ("pantry", "Pantry"),
                            ("fuel", "Fuel"),
                            ("office_expense", "Office Expense"),
                            ("site_development", "Site Development"),
                            ("site_visit", "Site Visit"),
                            ("printing", "Printing"),
                            ("utility", "Utility"),
                            ("others", "Others"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "custom_activity",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("remark", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
