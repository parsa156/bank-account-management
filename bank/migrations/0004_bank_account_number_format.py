# Generated by Django 5.1 on 2024-10-08 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_alter_bank_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='account_number_format',
            field=models.CharField(default='xxxxxxxxxxxxxxxxxx', max_length=16),
        ),
    ]
