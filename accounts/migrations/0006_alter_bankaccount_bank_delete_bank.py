# Generated by Django 5.1 on 2024-09-23 20:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_bankaccount_bank_name'),
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='bank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='bank.bank'),
        ),
        migrations.DeleteModel(
            name='Bank',
        ),
    ]
