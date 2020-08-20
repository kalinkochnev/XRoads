# Generated by Django 3.0.8 on 2020-08-18 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('XroadsAPI', '0002_auto_20200817_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='DistrictDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=20, unique=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='XroadsAPI.District')),
            ],
        ),
    ]