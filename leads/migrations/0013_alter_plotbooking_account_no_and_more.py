# Generated by Django 5.1.1 on 2024-10-15 06:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("leads", "0012_alter_plotbooking_project_alter_plotbooking_promoter"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plotbooking",
            name="account_no",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="plotbooking",
            name="bank_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="plotbooking",
            name="custom_gender",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="plotbooking",
            name="father_husband_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="plotbooking",
            name="gender",
            field=models.CharField(
                choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="plotbooking",
            name="location",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="plotbooking",
            name="mode_of_payment",
            field=models.CharField(
                choices=[("cheque", "Cheque"), ("rtgs", "RTGS/NEFT"), ("cash", "Cash")],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="plotbooking",
            name="nominee_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="plotbooking",
            name="payment_type",
            field=models.CharField(
                choices=[("custom", "Custom Payment"), ("installment", "Installments")],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="plotbooking",
            name="project",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="leads.project",
            ),
        ),
        migrations.AlterField(
            model_name="plotbooking",
            name="promoter",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="leads.promoter",
            ),
        ),
    ]
