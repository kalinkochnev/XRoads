# Generated by Django 2.2.4 on 2019-09-07 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('forum', '0024_auto_20190907_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_class',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.PROTECT,
                                    to='forum.SchoolClass'),
        ),
    ]
