# Generated by Django 4.2.6 on 2024-04-08 16:56

from django.db import migrations, models
import webflut.models


class Migration(migrations.Migration):

    dependencies = [
        ('webflut', '0065_activities_add_children'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step1model',
            name='first_name',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='step1model',
            name='last_name',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='step3model',
            name='height',
            field=models.IntegerField(default='', validators=[webflut.models.validate_height]),
        ),
        migrations.AlterField(
            model_name='step3model',
            name='weight',
            field=models.IntegerField(default='', validators=[webflut.models.validate_weight]),
        ),
    ]
