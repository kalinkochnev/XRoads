# Generated by Django 2.2.4 on 2019-09-07 13:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('forum', '0025_post_post_class'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subforum',
            old_name='subject_name',
            new_name='name',
        ),
    ]