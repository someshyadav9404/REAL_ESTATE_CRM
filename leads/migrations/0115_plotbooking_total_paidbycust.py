# Generated by Django 4.2.5 on 2024-11-12 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0114_remove_bill_tax_percentage"),
    ]

    operations = [
        migrations.AddField(
            model_name="plotbooking",
            name="total_paidbycust",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
