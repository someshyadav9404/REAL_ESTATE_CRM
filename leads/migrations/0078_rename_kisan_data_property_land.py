# Generated by Django 4.2.5 on 2024-11-02 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0077_remove_property_development_cost_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="property",
            old_name="kisan_data",
            new_name="land",
        ),
    ]
