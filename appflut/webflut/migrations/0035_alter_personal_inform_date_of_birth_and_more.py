# Generated by Django 4.2.4 on 2023-10-30 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webflut', '0034_personal_inform_first_name_personal_inform_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personal_inform',
            name='date_of_birth',
            field=models.FloatField(default='12'),
        ),
        migrations.AlterField(
            model_name='personal_inform',
            name='height',
            field=models.FloatField(default='12'),
        ),
        migrations.AlterField(
            model_name='personal_inform',
            name='weight',
            field=models.FloatField(default='12'),
        ),
    ]