# Generated by Django 5.1.2 on 2024-10-16 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0018_plotbooking_emi_amount_plotbooking_emi_tenure_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=255)),
                ('block', models.CharField(max_length=2)),
            ],
        ),
    ]