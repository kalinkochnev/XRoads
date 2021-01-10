# Generated by Django 3.1 on 2020-10-16 02:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('img', models.ImageField(upload_to='')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='XroadsAPI.district')),
            ],
        ),
        migrations.CreateModel(
            name='DistrictDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=20, unique=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='XroadsAPI.district')),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('main_img', models.ImageField(upload_to='')),
                ('is_visible', models.BooleanField(default=False)),
                ('presentation_url', models.URLField()),
                ('hidden_info', models.TextField(blank=True, null=True)),
                ('code', models.CharField(max_length=30)),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='XroadsAPI.school')),
            ],
        ),
    ]
