# Generated by Django 3.1 on 2020-11-06 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('XroadsAPI', '0007_auto_20201101_2201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='club',
            old_name='hidden_info',
            new_name='extra_info',
        ),
    ]
