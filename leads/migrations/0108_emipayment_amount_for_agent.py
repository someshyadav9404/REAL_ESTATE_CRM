# Generated by Django 4.2.5 on 2024-11-11 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0107_remove_billitem_bill_remove_billitem_product_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="emipayment",
            name="amount_for_agent",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
