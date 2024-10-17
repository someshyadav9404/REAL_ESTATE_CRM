# Generated by Django 5.1.1 on 2024-10-15 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0013_alter_plotbooking_account_no_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plotbooking",
            name="gender",
            field=models.CharField(
                choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
                max_length=10,
                null=True,
            ),
        ),
    ]