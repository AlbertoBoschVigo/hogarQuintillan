# Generated by Django 3.0.4 on 2020-04-17 14:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memos', '0009_auto_20200417_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memo',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default='', max_length=50), blank=True, default=list, null=True, size=None),
        ),
    ]
