# Generated by Django 3.1 on 2020-09-24 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('XroadsAuth', '0006_auto_20200915_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvitedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('roles', models.ManyToManyField(blank=True, to='XroadsAuth.RoleModel')),
            ],
        ),
    ]