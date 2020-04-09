# Generated by Django 3.0.4 on 2020-04-09 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recetas', '0002_auto_20200409_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingrediente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
                ('tipoMedida', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='IngredienteReceta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.CharField(max_length=64)),
                ('ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nombreIngrediente', to='recetas.Ingrediente')),
            ],
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
                ('elaboracion', models.TextField()),
                ('ingredientes', models.ManyToManyField(blank=True, related_name='ingredientes', to='recetas.IngredienteReceta')),
            ],
        ),
    ]
