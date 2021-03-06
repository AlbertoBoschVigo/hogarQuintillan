# Generated by Django 3.0.4 on 2020-04-09 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0004_auto_20200409_1316'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=64)),
            ],
        ),
        migrations.RemoveField(
            model_name='ingredientereceta',
            name='recetas',
        ),
        migrations.AddField(
            model_name='ingredientereceta',
            name='receta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receta', to='recetas.Receta'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='receta',
            name='comensales',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='receta',
            name='descripcion',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='receta',
            name='dificultad',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='receta',
            name='tiempoPreparacion',
            field=models.DurationField(blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='receta',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categoria', to='recetas.Categoria'),
            preserve_default=False,
        ),
    ]
