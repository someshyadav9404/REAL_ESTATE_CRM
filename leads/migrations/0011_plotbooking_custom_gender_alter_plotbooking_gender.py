# Generated by Django 5.1.1 on 2024-10-15 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0010_plotbooking"),
    ]

    operations = [
        migrations.AddField(
            model_name="plotbooking",
            name="custom_gender",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="plotbooking",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
                max_length=10,
                null=True,
            ),
        ),
    ]
