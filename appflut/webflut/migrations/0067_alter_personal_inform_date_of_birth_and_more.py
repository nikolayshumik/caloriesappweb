# Generated by Django 4.2.6 on 2024-04-14 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webflut', '0066_alter_step1model_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personal_inform',
            name='date_of_birth',
            field=models.DateField(default='1990-01-01'),
        ),
        migrations.AlterField(
            model_name='step1model',
            name='date_of_birth',
            field=models.DateField(default='1990-01-01'),
        ),
    ]
