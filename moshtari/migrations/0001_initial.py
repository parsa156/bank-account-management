# Generated by Django 5.1 on 2024-09-01 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('Email', models.EmailField(max_length=200)),
                ('code_meli', models.CharField(max_length=10)),
                ('Pasword', models.CharField(max_length=20)),
            ],
        ),
    ]
