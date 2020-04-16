from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _

from django.contrib.postgres.fields import ArrayField

import logging
from datetime import date, datetime, timedelta

logger = logging.getLogger(__name__)

# Create your models here.

class Memo(models.Model):
    
    class Categoria(models.TextChoices):
        PERSONAL = 'pe', _('Personal')
        LABORAL = 'ta', _('Laboral')
        FAMILIAR = 'fa', _('Familiar')

    titulo = models.CharField(max_length=100)
    creador = models.ForeignKey(User, related_name="creador", on_delete=models.CASCADE)
    dirigido = models.ManyToManyField(User, related_name="dirigido")
    detalle = models.CharField(max_length=1000)
    categoria = models.CharField(max_length=2, choices=Categoria.choices)
    tags = ArrayField(models.CharField(max_length=50, blank=True), default = list)
    cita = models.BooleanField(default=False)
    fecha_cita = models.DateTimeField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_limite = models.DateTimeField(blank=True)
    padre = models.ForeignKey('self', on_delete=models.CASCADE, blank=True)
    hijo = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True)

    def save(self, *args, **kwargs):
        if self.cita and not self.fecha_cita:
            logger.info('Tried to set cita without date')
            return 
        else:
            super().save(*args, **kwargs)

    def day(self):
        # Devuelve True si la fecha limite es hoy
        if self.fecha_limite:
            return self.fecha_limite.date() == datetime.now().date()
        return False

    def week(self):
        # Devuelve True si la fecha limite es esta semana
        if self.fecha_limite:
            return self.fecha_limite.date() <= datetime.now().date() + timedelta(days=6-date.today().weekday())
        return False

    def __str__(self):
        return f'Memo: { self.titulo } , de { self.creador } dirigida a { self.dirigido }'

