# Generated by Django 4.2.7 on 2023-12-03 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webflut', '0052_breakfast_products_calories_in_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='breakfast_products',
            old_name='calories_in',
            new_name='calories',
        ),
    ]