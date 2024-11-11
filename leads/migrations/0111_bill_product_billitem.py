# Generated by Django 4.2.5 on 2024-11-11 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0110_remove_invoice_customer_remove_invoice_items_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Bill",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "bill_number",
                    models.CharField(blank=True, max_length=20, unique=True),
                ),
                ("buyer_name", models.CharField(max_length=255)),
                ("buyer_address", models.TextField()),
                ("buyer_pan_number", models.CharField(max_length=20)),
                ("buyer_state", models.CharField(max_length=50)),
                ("invoice_date", models.DateField()),
                ("due_date", models.DateField()),
                (
                    "total_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=15),
                ),
                (
                    "tax_percentage",
                    models.DecimalField(decimal_places=2, default=0, max_digits=5),
                ),
                (
                    "other_charges",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="BillItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.CharField(max_length=255)),
                ("quantity", models.PositiveIntegerField()),
                ("rate", models.DecimalField(decimal_places=2, max_digits=10)),
                ("tax", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "total_price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=15),
                ),
                (
                    "bill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="leads.bill",
                    ),
                ),
            ],
        ),
    ]
