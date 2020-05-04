from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.views.decorators.cache import cache_page

from .models import Receta, IngredienteReceta, Categoria, Ingrediente

from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from hogarQuintillan.clase_contexto import contextoBase


from .forms import IngredienteInlineFormset, IngredienteRecetaForm, IngredientesFormset, IngredientesFormsetDelete, RecetaForm

import logging

# Create your views here.

logger = logging.getLogger(__name__)

@cache_page(60 * 15)
def index(request):
    listaCat = []
    try:
        categorias = Categoria.objects.all()
        logger.debug(f'Categorias disponibles: {categorias}')
        for categoria in categorias:
            listaCat.append(categoria.nombre)

        _context = contextoBase(categorias = listaCat)
        return render(request, "recetas/recetas_index.html", _context.get())
    except Exception as e:
        logger.debug(e)
        return HttpResponse('Activo')

class CategoriaListView(ListView):
    model = Categoria
    template_name= "recetas/recetas_index.html"
    context_object_name = 'categorias'

@cache_page(60 * 15)
def receta(request, idReceta, categoria = ''):
    try:
        receta = Receta.objects.get(pk=idReceta)
        ingredientes = IngredienteReceta.objects.all().filter(receta_id=idReceta)
        categorias = Categoria.objects.all()
    except Receta.DoesNotExist:
        logger.info(f'Receta {idReceta} solicitada no existe')
        raise Http404("Esa receta no existe")
    if categoria != '' and categoria != str(receta.categoria):
        raise Http404("Esa receta no cuadra en esta categoria")
    
    _context = contextoBase(receta = receta, ingredientes = ingredientes, categorias = categorias, categoria = str(receta.categoria))

    return render(request, "recetas/receta.html", _context.get())

class RecetaListView(ListView):
    model = Receta
    template_name= "recetas/recetas_categorias.html"
    context_object_name = 'recetas'

    def get_queryset(self):
        self.queryset = super().get_queryset()
        return self.queryset.filter(categoria__nombre=self.kwargs['categoria'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class RecetaDetailView(DetailView):
    model = Receta
    template_name= "recetas/receta.html"
    context_object_name = 'receta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categorias = Categoria.objects.all()
        context['categorias'] = categorias
        return context

class RecetaCreateView(LoginRequiredMixin, CreateView):
    model = Receta
    template_name="recetas/receta_form.html"
    context_object_name="receta"
    form_class = RecetaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['namePag'] = "Crear"
        logger.error(context)
        return context

    def get_success_url(self):
        return reverse("recetas:index")

class RecetaUpdateView(LoginRequiredMixin, UpdateView):
    model = Receta
    template_name="recetas/receta_form.html"
    context_object_name="receta"
    form_class = RecetaForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["form"] = self.form_class(self.request.POST)
        else:

            context["form"] = self.form_class(instance=self.model.objects.get(pk=self.kwargs['pk']))
        context['namePag'] = "Editar"
        logger.error(context)
        return context

    def get_success_url(self):
        return reverse("recetas:index")

class RecetaDeleteView(LoginRequiredMixin, DeleteView):
    model = Receta
    success_url = reverse_lazy('recetas:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.ingredientes_recetas.all().delete()
        self.object.delete()
        return HttpResponseRedirect(success_url)

class OldRecetaCreateView(CreateView):
    model = Receta
    fields = '__all__'
    template_name="recetas/receta_form.html"
    context_object_name="receta"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["ingrediente"] = IngredientesFormset(self.request.POST)
        else:
            context["ingrediente"] = IngredientesFormset(queryset=IngredienteReceta.objects.none())
        context['namePag'] = "Crear"
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingredientes = context["ingrediente"]
        self.object = form.save()
        if ingredientes.is_valid():
            ingredientes.instance = self.object
            ingredientes.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("recetas:index")

class OldRecetaUpdateView(UpdateView):
    model = Receta
    fields = '__all__'
    template_name="recetas/receta_form.html"
    context_object_name="receta"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["ingrediente"] = IngredientesFormsetDelete(self.request.POST)
        else:
            logger.error(IngredienteReceta.objects.filter(receta=self.kwargs['pk']).values('ingrediente_id', 'ingrediente__nombre', 'cantidad'))
            context["ingrediente"] = IngredientesFormsetDelete(queryset= IngredienteReceta.objects.filter(receta=self.kwargs['pk']), initial= IngredienteReceta.objects.filter(receta=self.kwargs['pk']).values('ingrediente__nombre', 'cantidad'))
        context['namePag'] = "Editar"
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingrediente = context["ingrediente"]
        self.object = form.save()
        
        if ingrediente.is_valid():
            resultado = ingrediente.save(commit=False)
            logger.error('Form valid')
            for obj in ingrediente.deleted_objects:
                obj.delete()
            for i in resultado:
                i.receta = Receta.objects.get(pk=self.kwargs['pk'])
                i.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("recetas:index")

class IngredienteCreateView(CreateView):
    model = Ingrediente
    fields = '__all__'
    template_name="recetas/ingrediente.html"
    context_object_name="ingrediente"
    success_url= reverse_lazy('recetas:ingrediente_validado')

class IngredienteValidado(TemplateView):
    template_name="recetas/ingrediente_validado.html"

@cache_page(60 * 15)
def categoria(request, categoria):
    if categoria == 'todas':
        return HttpResponseRedirect(reverse("recetas:index", args =[]))
    else:
        try:
            cat = Categoria.objects.get(nombre= categoria)
        except Categoria.DoesNotExist:
            logger.info(f'Categoria {categoria} solicitada no existe')
            raise Http404("Esa categoria no existe")
        _context = contextoBase(categoria = cat.nombre)

    return render(request, "recetas/recetas_categorias.html", _context.get())