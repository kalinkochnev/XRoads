# Generated by Django 2.2.4 on 2019-09-07 22:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('forum', '0030_auto_20190907_2241'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='post_class',
            new_name='post_school_class',
        ),
    ]