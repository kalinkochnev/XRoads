# Generated by Django 3.0.8 on 2020-08-15 01:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('XroadsAPI', '0002_auto_20200813_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='XroadsAPI.District'),
        ),
    ]
