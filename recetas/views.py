from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Receta, IngredienteReceta, Categoria

import logging

# Create your views here.

logger = logging.getLogger(__name__)

def index(request):
    listaCat = []
    try:
        categorias = Categoria.objects.all()
        logger.debug(f'Categorias disponibles: {categorias}')
        for categoria in categorias:
            listaCat.append(categoria.nombre)
        context = {
            'categorias': listaCat
        }
        return render(request, "recetas/recetas_index.html", context)
    except:
        return HttpResponse('Activo')

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

    context = {
        "receta": receta,
        "ingredientes": ingredientes,
        "categorias": categorias,
        "categoria":str(receta.categoria)
    }
    return render(request, "recetas/receta.html", context)

def categoria(request, categoria):
    if categoria == 'todas':
        return HttpResponseRedirect(reverse("recetas_index", args =[]))
    else:
        try:
            cat = Categoria.objects.get(nombre= categoria)
        except Categoria.DoesNotExist:
            logger.info(f'Categoria {categoria} solicitada no existe')
            raise Http404("Esa categoria no existe")
        context = {
            "categoria": cat.nombre
        }

    return render(request, "recetas/recetas_categorias.html", context)