# Generated by Django 2.2.4 on 2019-09-29 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0034_auto_20190929_0116'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolclass',
            name='subject',
            field=models.CharField(default='Subject thing', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schoolclass',
            name='placement',
            field=models.CharField(max_length=15),
        ),
    ]
