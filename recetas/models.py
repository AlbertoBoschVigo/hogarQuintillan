from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import timedelta

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.nombre}'


class Ingrediente(models.Model):
    MEDIDA = [
        ('gr', 'gramos'),
        ('ml', 'mililitros'),
        ('kg', 'kilogramos'),
        ('li', 'litros'),
        ('cu', 'cucharada'),
        ('ci', 'cucharadita'),
    ]
    nombre = models.CharField(max_length=64)
    tipoMedida = models.CharField(max_length=64, choices=MEDIDA)

    def __str__(self):
        return f'{self.nombre} - {self.tipoMedida}'


class Receta(models.Model):
    DIFICULTAD = [
        ('ri', 'Ridicula'),
        ('ba', 'Baja'),
        ('mo', 'Moderada'),
        ('di', 'Dificil'),
        ('md', 'Muy dificil'),
        ('in', 'Infernal')
    ]
    nombre = models.CharField(max_length=64)
    descripcion = models.CharField(max_length=64, blank=True)
    elaboracion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="categoria")
    dificultad = models.CharField(max_length=64, blank=True, choices=DIFICULTAD)
    comensales = models.IntegerField(default=2)
    tiempoPreparacion = models.DurationField(blank=True, default=timedelta(hours=2))
    etiquetas = ArrayField(models.CharField(max_length=24, blank=True), default = list)

    def __str__(self):
        return f'{self.nombre}.\n- {self.descripcion}'


class IngredienteReceta(models.Model):
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE, related_name="ingrediente")
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name="receta")
    cantidad = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.ingrediente} - {self.cantidad} - {self.receta}'

