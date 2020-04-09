from django.contrib import admin
from .models import Categoria, Ingrediente, IngredienteReceta, Receta
# Register your models here.

class IngredienteRecetaInline(admin.StackedInline):
    model = IngredienteReceta
    extra = 5

class RecetaAdmin(admin.ModelAdmin):
    inlines = [IngredienteRecetaInline]

admin.site.register(Categoria)
admin.site.register(Ingrediente)
admin.site.register(Receta, RecetaAdmin)
