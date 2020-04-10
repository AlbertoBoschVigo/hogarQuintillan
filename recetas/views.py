from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from .models import Receta, IngredienteReceta, Categoria

# Create your views here.

def index(request):
    return HttpResponse('Activo')

def receta(request, idReceta, categoria = ''):
    try:
        receta = Receta.objects.get(pk=idReceta)
        ingredientes = IngredienteReceta.objects.all().filter(receta_id=idReceta)
        categorias = Categoria.objects.all()
    except Receta.DoesNotExist:
        raise Http404("Esa receta no existe")
    if categoria != '' and categoria != str(receta.categoria):
        print(categoria)
        print(receta.categoria)
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
            raise Http404("Esa categoria no existe")
        context = {
            "categoria": cat.nombre
        }

    return render(request, "recetas/recetas_categorias.html", context)