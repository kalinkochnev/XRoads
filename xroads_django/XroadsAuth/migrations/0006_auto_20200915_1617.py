# Generated by Django 3.1 on 2020-09-15 16:17

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('XroadsAuth', '0005_auto_20200913_1655'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=200)),
                ('perms', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='hierarchy_perms',
        ),
        migrations.DeleteModel(
            name='HierarchyPerms',
        ),
        migrations.AddField(
            model_name='profile',
            name='roles',
            field=models.ManyToManyField(blank=True, to='XroadsAuth.RoleModel'),
        ),
    ]
