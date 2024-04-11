# Generated by Django 4.2.6 on 2024-04-03 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webflut', '0063_delete_activity_for_children'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity_for_children',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('subcategory', models.CharField(max_length=255)),
                ('code_6_9', models.CharField(max_length=255)),
                ('code_10_12', models.CharField(max_length=255)),
                ('code_13_15', models.CharField(max_length=255)),
                ('code_16_18', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Виды Детских Активностей ',
                'verbose_name_plural': 'Виды Детских Активностей',
            },
        ),
    ]