from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name = "vera_index"),
    path("tareas", views.tareas, name = "vera_tareas"),
    path("calendario", views.calendario, name = "vera_calendario")
]