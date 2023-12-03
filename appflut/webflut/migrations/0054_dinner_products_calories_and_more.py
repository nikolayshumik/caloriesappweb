# Generated by Django 4.2.7 on 2023-12-03 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webflut', '0053_rename_calories_in_breakfast_products_calories'),
    ]

    operations = [
        migrations.AddField(
            model_name='dinner_products',
            name='calories',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='dinner_products',
            name='carbohydrates',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='dinner_products',
            name='fats',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='dinner_products',
            name='proteins',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='lunch_products',
            name='calories',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='lunch_products',
            name='carbohydrates',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='lunch_products',
            name='fats',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='lunch_products',
            name='proteins',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='snack_products',
            name='calories',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='snack_products',
            name='carbohydrates',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='snack_products',
            name='fats',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='snack_products',
            name='proteins',
            field=models.FloatField(default=0),
        ),
    ]
