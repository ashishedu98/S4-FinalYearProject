# Generated by Django 3.2.3 on 2021-05-31 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secapp', '0011_auto_20210529_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suspect_profiles',
            name='last_found',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='suspect_recognised',
            name='detect_time',
            field=models.CharField(max_length=100),
        ),
    ]