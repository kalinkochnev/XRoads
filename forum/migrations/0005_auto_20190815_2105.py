# Generated by Django 2.2.2 on 2019-08-15 21:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('forum', '0004_auto_20190812_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subforum',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]