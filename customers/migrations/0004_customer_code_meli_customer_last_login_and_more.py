# Generated by Django 5.1 on 2024-10-08 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0003_alter_customer_email_alter_customer_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='code_meli',
            field=models.CharField(default='00000000', max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(default='11111111', max_length=20),
        ),
        migrations.AddField(
            model_name='customer',
            name='username',
            field=models.CharField(default='default_user', max_length=150, unique=True),
        ),
    ]
