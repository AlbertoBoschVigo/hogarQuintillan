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
        return Memo.objects.filter(
            Q(fecha_limite__lt=tomorrow)|Q(fecha_limite__isnull=True)
        )

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
    fields = ['titulo', 'dirigido', 'detalle', 'categoria', 'tags', 'cita', 'fecha_cita', 'fecha_limite', 'padre']

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
    fields = ['detalle', 'tags', 'fecha_cita','fecha_limite', 'padre', 'completada', 'ignorar']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar'
        logger.info(context)
        return context

    def get_initial(self, **kwargs):
        initial = super().get_initial(**kwargs)
        logger.info(initial)
        return initial

    def get_form(self, **kwargs):
        logger.info('GET_FORM')
        form = super().get_form(**kwargs)
        for row in form:
            for col in row:
                logger.info(col)
        return form

    def get_form_class(self, **kwargs):
        form = super().get_form_class(**kwargs)
        logger.info('GET_FORM_CLASS')
        logger.info(form)
        return form

    def form_valid(self, form):
        form.instance.creador = self.request.user
        return super().form_valid(form)

class MemoDelete(LoginRequiredMixin, DeleteView):
    model = Memo
    success_url = reverse_lazy('memos:list')

    def form_valid(self, form):
        form.instance.creador = self.request.user
        return super().form_valid(form)