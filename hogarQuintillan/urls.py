"""hogarQuintillan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

class contextoBase():
    def __init__(self, **kwargs):
        topHeader = [
            ('calendarioGlobal', 'Calendario'),
            ('chat_index', 'Chat'),
            ('recetas_index', 'Recetas'),
            ('vera_tareas', 'TareasV')
        ]
        rutaInicio = ('index', 'Inicio')
        self.contextoBase = {
            'topHeader': topHeader,
            'inicio': rutaInicio,
            'pageTitle':'Hogar Quintillan'
        }
        self.add(**kwargs)
    
    def add(self, **kwargs):
        for k,v in kwargs.items():
            self.contextoBase[k] = v
    
    def get(self):
        return self.contextoBase

from . import views
urlpatterns = [
    path("", views.index, name = "index"),
    path("calendario", views.calendarioGlobal, name = "calendarioGlobal"),
    path('admin/', admin.site.urls),
    path('vera/', include("veraPage.urls")),
    path('chat/', include("chat.urls")),
    path('recetas/', include("recetas.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/registro/", views.registro, name = "registro"),
]