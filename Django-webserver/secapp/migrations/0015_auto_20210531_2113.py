# Generated by Django 3.2.3 on 2021-05-31 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secapp', '0014_auto_20210531_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='suspect_profiles',
            name='cases',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='suspect_profiles',
            name='date_of_birth',
            field=models.CharField(help_text='Format:YYYY-MM-DD', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='suspect_profiles',
            name='detect_time',
            field=models.CharField(default='2021-05-31 21:13:05', help_text='Format: YYYY-MM-DD HH:MM:SS', max_length=100),
        ),
        migrations.AlterField(
            model_name='suspect_recognised',
            name='detect_time',
            field=models.CharField(default='2021-05-31 21:13:05', help_text='Format: YYYY-MM-DD HH:MM:SS', max_length=100),
        ),
    ]
