# Generated by Django 3.0.4 on 2020-04-20 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memos', '0012_auto_20200419_1958'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='memo',
            options={'ordering': ['prioridad', 'fecha_creacion']},
        ),
        migrations.AlterField(
            model_name='memo',
            name='prioridad',
            field=models.IntegerField(choices=[(1, 'Alta'), (2, 'Normal'), (3, 'Baja')], default=2, null=True),
        ),
    ]