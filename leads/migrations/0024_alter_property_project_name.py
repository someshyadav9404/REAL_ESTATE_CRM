# Generated by Django 5.1.2 on 2024-10-16 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0023_property_project_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='project_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
