from django.db import models
from django.conf import settings

from django.utils.translation import gettext_lazy as _

from django.contrib.postgres.fields import ArrayField

import logging
from datetime import date, datetime, timedelta

logger = logging.getLogger(__name__)

# Create your models here.
"""
    Ej queries:

    usuario.memos_creados.all()
        <QuerySet [<Memo: Memo: titulo del memo>, <Memo: Memo: Memo sin dirigido>]>
    User.objects.all()
        <QuerySet [<User: prueba>, <User: alberto>, <User: albertito>, <User: vera>, <User: prueba2>]>
    memos = Memo.objects.order_by("creador")[0:8] 
    memos = Memo.objects.order_by("creador").values_list("creador")
    User.objects.order_by("memos_creados")

    print([m.id for m in User.objects.order_by("memos_creados")])
"""

class Memo(models.Model):
    
    class Categoria(models.TextChoices):
        PERSONAL = 'pe', _('Personal')
        LABORAL = 'ta', _('Laboral')
        FAMILIAR = 'fa', _('Familiar')

    class Prioridad(models.TextChoices):
        ALTA = 'al', _('Alta')
        NORMAL = 'no', _('Normal')
        BAJA = 'ba', _('Baja')

    # %(class)s
    titulo = models.CharField(max_length=100, verbose_name="Titulo")
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="memos_creados", on_delete=models.CASCADE, verbose_name="Creado por")
    dirigido = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="memos_dirigidos")
    detalle = models.TextField(max_length=1000, verbose_name="Detalle")
    categoria = models.CharField(max_length=2, choices=Categoria.choices, default=Categoria.PERSONAL, null=True, verbose_name="Categoria")
    tags = ArrayField(models.CharField(max_length=50, default=''), default = list, null=True, blank=True)
    cita = models.BooleanField(default=False, verbose_name="Cita")
    fecha_cita = models.DateTimeField(blank=True, null=True, verbose_name="Fecha cita")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Modificado el")
    fecha_limite = models.DateTimeField(blank=True, null=True, verbose_name="Fecha limite")
    padre = models.ForeignKey('self', related_name='hijos', on_delete=models.CASCADE, blank=True, null=True)
    completada = models.BooleanField(default=False, verbose_name="Completada")
    ignorar = models.BooleanField(default=False, verbose_name="Ignorar")
    prioridad = models.CharField(max_length=2, choices=Prioridad.choices, default=Prioridad.NORMAL, null=True)
    dirigidos = []

    class Meta:
        ordering = ['fecha_creacion']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('memos:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if self.cita and not self.fecha_cita:
            logger.info('Tried to set cita without date')
            return

        if self.fecha_cita and not self.fecha_limite:
            self.fecha_limite = self.fecha_cita

        super().save(*args, **kwargs)
        if len(self.dirigidos) < 1:
            self.dirigidos.append(self.creador)
        for _ in self.dirigidos:
            self.dirigido.add(_)

    def get_dicc(self):
        dicc = {}
        for key in self._meta.get_fields():
            aux = getattr(self, key.name)
            dicc[key.name] = (aux, str(type(aux)).replace("'>","").replace("<class '", ""))
        
        return dicc

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
        return f'{ self.titulo }'

