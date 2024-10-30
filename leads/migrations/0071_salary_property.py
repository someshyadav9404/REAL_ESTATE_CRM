# Generated by Django 4.2.5 on 2024-10-30 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0070_kisan_is_sold"),
    ]

    operations = [
        migrations.AddField(
            model_name="salary",
            name="property",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="leads.property",
            ),
        ),
    ]
