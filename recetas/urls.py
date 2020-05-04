from django.urls import path

from . import views

app_name = "recetas"
urlpatterns = [
    path("", views.CategoriaListView.as_view(), name = "index"),
    path("<str:categoria>/<int:pk>/", views.RecetaDetailView.as_view(), name="receta"),
    path("<str:categoria>/", views.RecetaListView.as_view(), name="categoria"),
    path("crear/nueva/", views.RecetaCreateView.as_view(), name="crear"),
    path("<str:categoria>/<int:pk>/editar/", views.RecetaUpdateView.as_view(), name="editar"),
    path("<str:categoria>/<int:pk>/borrar/", views.RecetaDeleteView.as_view(), name="borrar"),
    path("crear/ingrediente/", views.IngredienteCreateView.as_view(), name="crear_ingrediente"),
    path("crear/ingrediente/creado/", views.IngredienteValidado.as_view(), name="ingrediente_validado"),
]