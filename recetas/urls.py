from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name = "recetas_index"),
    path("<int:idReceta>", views.receta, name="recetas_receta"),
    path("<str:categoria>", views.categoria, name="recetas_categoria"),
]