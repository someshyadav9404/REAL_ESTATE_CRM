# Generated by Django 5.1.2 on 2024-10-15 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0009_merge_0007_promoter_0008_alter_property_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='property',
            name='title',
            field=models.CharField(max_length=7),
        ),
    ]