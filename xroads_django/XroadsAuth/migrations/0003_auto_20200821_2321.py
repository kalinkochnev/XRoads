# Generated by Django 3.1 on 2020-08-21 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('XroadsAuth', '0002_auto_20200817_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
