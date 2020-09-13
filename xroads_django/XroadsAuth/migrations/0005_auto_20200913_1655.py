# Generated by Django 3.1 on 2020-09-13 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('XroadsAPI', '0005_club_join_promo'),
        ('XroadsAuth', '0004_profile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='XroadsAPI.school'),
        ),
    ]
