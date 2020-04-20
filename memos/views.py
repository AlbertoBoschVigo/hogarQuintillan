from .models import Memo
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from django.db.models import Q

from django.conf import settings

import logging
#from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


# Create your views here.

"""
class MemoList(LoginRequiredMixin, ListView):
    model = Memo
    template_name = 'memos/memo_list.html'

    def get_queryset(self):
        self.usuario = get_object_or_404(User, username=self.request.user)
        return Memo.objects.filter(creador=self.usuario)

"""

class MemoList(ListView):
    def get_queryset(self):
        from django.utils import timezone
        import datetime
        tomorrow = timezone.now().date() + datetime.timedelta(days=1)
        if settings.DEBUG or self.request.user.is_authenticated:
            return Memo.objects.filter(
                Q(fecha_limite__lt=tomorrow)|Q(fecha_limite__isnull=True)
            )
        else:
            return Memo.objects.none()

class MemoDetail(DetailView):
    model = Memo
    #fields = ['titulo', 'dirigido', 'detalle', 'categoria', 'tags', 'cita', 'fecha_cita', 'fecha_limite', 'padre']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """
        hijos = Memo.objects.filter(padre_id=self.object.id)
        context['hijos'] = hijos
        for hijo in hijos:
            logger.info(hijo.titulo)
        """
        return context

class MemoCreation(LoginRequiredMixin, CreateView):
    model = Memo
    success_url = reverse_lazy('memos:list')
    fields = ['titulo', 'dirigido', 'detalle', 'categoria', 'prioridad', 'tags', 'cita', 'fecha_cita', 'fecha_limite', 'padre']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear'
        return context

    def form_valid(self, form):
        form.instance.creador = self.request.user
        return super().form_valid(form)

class MemoUpdate(LoginRequiredMixin, UpdateView):
    model = Memo
    success_url = reverse_lazy('memos:list')
    fields = ['detalle', 'tags', 'fecha_cita','fecha_limite','prioridad', 'padre', 'completada', 'ignorar']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar'
        return context

    def get_initial(self, **kwargs):
        initial = super().get_initial(**kwargs)
        return initial

    def form_valid(self, form):
        form.instance.creador = self.request.user
        return super().form_valid(form)

class MemoDelete(LoginRequiredMixin, DeleteView):
    model = Memo
    success_url = reverse_lazy('memos:list')

    def form_valid(self, form):
        form.instance.creador = self.request.user
        return super().form_valid(form)