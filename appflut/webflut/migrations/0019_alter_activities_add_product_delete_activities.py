# Generated by Django 4.2.4 on 2023-10-20 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webflut', '0018_activities_alter_activities_add_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activities_add',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webflut.activity'),
        ),
        migrations.DeleteModel(
            name='Activities',
        ),
    ]