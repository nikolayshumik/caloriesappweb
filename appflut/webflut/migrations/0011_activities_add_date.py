# Generated by Django 4.2.4 on 2023-10-18 19:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webflut', '0010_ttime_test_delete_time_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='activities_add',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
