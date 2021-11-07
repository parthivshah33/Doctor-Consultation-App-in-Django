# Generated by Django 3.1.7 on 2021-07-03 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('am', '0017_auto_20210703_2355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointments',
            name='confirm_case',
        ),
        migrations.AddField(
            model_name='appointments',
            name='confirm',
            field=models.PositiveIntegerField(default=0, max_length=6),
        ),
    ]