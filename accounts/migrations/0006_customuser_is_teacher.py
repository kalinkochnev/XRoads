# Generated by Django 2.2.4 on 2019-09-07 12:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0005_auto_20190722_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_teacher',
            field=models.BooleanField(default=False),
        ),
    ]
