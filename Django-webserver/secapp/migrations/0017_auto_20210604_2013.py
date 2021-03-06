# Generated by Django 3.2 on 2021-06-04 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secapp', '0016_auto_20210531_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suspect_profiles',
            name='last_found',
            field=models.CharField(default='2021-06-04 20:13:25', help_text='Format: YYYY-MM-DD HH:MM:SS', max_length=100),
        ),
        migrations.AlterField(
            model_name='suspect_recognised',
            name='detect_time',
            field=models.CharField(default='2021-06-04 20:13:25', help_text='Format: YYYY-MM-DD HH:MM:SS', max_length=100),
        ),
    ]
