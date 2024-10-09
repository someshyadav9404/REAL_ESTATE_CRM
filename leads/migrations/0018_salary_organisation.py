# Generated by Django 5.1.1 on 2024-10-09 14:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0017_alter_agent_id_alter_bonus_id_alter_category_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="salary",
            name="organisation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="leads.userprofile",
            ),
        ),
    ]
