# Generated by Django 3.0.4 on 2020-04-09 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientereceta',
            name='ingrediente',
        ),
        migrations.RemoveField(
            model_name='receta',
            name='ingredientes',
        ),
        migrations.DeleteModel(
            name='Ingrediente',
        ),
        migrations.DeleteModel(
            name='IngredienteReceta',
        ),
        migrations.DeleteModel(
            name='Receta',
        ),
    ]
