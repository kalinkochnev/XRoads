# Generated by Django 2.2.4 on 2019-09-07 12:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0022_schoolclass_class_teachers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolclass',
            name='class_students',
            field=models.ManyToManyField(related_name='class_students', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='schoolclass',
            name='class_teachers',
        ),
        migrations.AddField(
            model_name='schoolclass',
            name='class_teachers',
            field=models.ManyToManyField(related_name='class_teachers', to=settings.AUTH_USER_MODEL),
        ),
    ]