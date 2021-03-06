# Generated by Django 3.0.4 on 2020-04-10 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0008_receta_etiquetas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingrediente',
            name='tipoMedida',
            field=models.CharField(choices=[('gr', 'gramos'), ('ml', 'mililitros'), ('kg', 'kilogramos'), ('li', 'litros'), ('cu', 'cucharada'), ('ci', 'cucharadita'), ('ud', 'unidades'), ('pl', 'pellizco'), ('pu', 'puñado'), ('ma', 'manojo')], max_length=64),
        ),
    ]
