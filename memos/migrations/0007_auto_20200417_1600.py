# Generated by Django 3.0.4 on 2020-04-17 14:00

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memos', '0006_auto_20200417_1231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='memo',
            options={'ordering': ['fecha_creacion']},
        ),
        migrations.AlterField(
            model_name='memo',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50, null=True), default=list, size=None),
        ),
    ]
