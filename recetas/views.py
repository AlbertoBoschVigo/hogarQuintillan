from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from django.views.decorators.cache import cache_page

from .models import Receta, IngredienteReceta, Categoria

from hogarQuintillan.clase_contexto import contextoBase

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
    
@cache_page(60 * 15)
def categoria(request, categoria):
    if categoria == 'todas':
        return HttpResponseRedirect(reverse("recetas_index", args =[]))
    else:
        try:
            cat = Categoria.objects.get(nombre= categoria)
        except Categoria.DoesNotExist:
            logger.info(f'Categoria {categoria} solicitada no existe')
            raise Http404("Esa categoria no existe")
        _context = contextoBase(categoria = cat.nombre)

    return render(request, "recetas/recetas_categorias.html", _context.get())