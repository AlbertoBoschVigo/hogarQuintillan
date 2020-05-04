from django.forms import ModelForm, modelformset_factory, CharField, IntegerField, ModelChoiceField
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from .models import Receta, IngredienteReceta, Ingrediente

import logging


logger = logging.getLogger(__name__)


class IngredienteForm(ModelForm):
    class Meta:
        model = IngredienteReceta
        fields=['ingrediente', 'cantidad']


class BaseIngredientesFormset(BaseInlineFormSet):
    pass

IngredienteInlineFormset = inlineformset_factory(
    Receta, IngredienteReceta, form=IngredienteForm, extra=10, can_delete=False
)

class IngredienteRecetaForm(ModelForm):
    class Meta:
        model = IngredienteReceta
        fields = ['ingrediente', 'cantidad']

IngredientesFormset = modelformset_factory(IngredienteReceta, fields=['ingrediente', 'cantidad'], extra=10, can_delete=False)

IngredientesFormsetDelete = modelformset_factory(IngredienteReceta, fields=['ingrediente', 'cantidad'], extra=10, can_delete=True)



class RecetaForm(ModelForm):
    class Meta:
        model = Receta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listado_campos = []
        try:
            ingredientes = self.instance.ingredientes_recetas.all()
        except:
            ingredientes = Receta.objects.none()
        for i in range(len(ingredientes) + 1):
            field_name = f'ingrediente_{i}'
            field_cantidad = f'cantidad_{i}'
            self.listado_campos.append(field_name)
            self.fields[field_name] = ModelChoiceField(queryset=Ingrediente.objects.all(), required=False)
            self.fields[field_cantidad] = IntegerField(required=False)
            try:
                self.initial[field_name] = ingredientes[i].ingrediente
                self.initial[field_cantidad] = ingredientes[i].cantidad
            except IndexError:
                self.initial[field_name] = ""
                self.initial[field_cantidad] = 0
        # create an extra blank field
        for i in range(1,4):
            field_name = f'ingrediente_{len(ingredientes) + i}'
            field_cantidad = f'cantidad_{len(ingredientes) + i}'
            self.listado_campos.append(field_name)
            self.fields[field_name] = ModelChoiceField(queryset=Ingrediente.objects.all(), required=False)
            self.fields[field_cantidad] = IntegerField(required=False)
        

    def save(self):
        receta = self.instance
        receta.save()

        receta.ingredientes_recetas.all().delete()
        for ingrediente, cantidad in self.cleaned_data['ingredientes'].items():
            IngredienteReceta.objects.create(receta=receta, ingrediente=ingrediente, cantidad=cantidad)
        """
        for i in range(1,4):
           ingrediente = self.cleaned_data[f'ingrediente_{i}']
           cantidad = self.cleaned_data[f'cantidad_{i}']
           IngredienteReceta.objects.create(
               receta=receta, ingrediente=ingrediente, cantidad=cantidad)
        """

    def clean(self):
        ingredientes = set()
        ing_cant = {}
        ii = 0
        for i in range(len(self.listado_campos)):
            field_name = f'ingrediente_{i}'
            field_cantidad = f'cantidad_{i}'
            if self.cleaned_data.get(field_name) and self.cleaned_data.get(field_cantidad):
                ingrediente = self.cleaned_data[field_name]
                cantidad = self.cleaned_data[field_cantidad]
                if ingrediente in ingredientes:
                    self.add_error(field_name, 'Duplicate')
                else:
                    ingredientes.add(ingrediente)
                    ing_cant[ingrediente] = cantidad
            ii+=1
        field_name = f'ingrediente_{ii}'
        field_cantidad = f'cantidad_{ii}'
        while self.data.get(field_name) and self.data.get(field_cantidad):
            ingrediente = Ingrediente.objects.get(pk=int(self.data[field_name]))
            cantidad = self.data[field_cantidad]
            if ingrediente in ingredientes:
                self.add_error(field_name, 'Duplicate')
            else:
                ingredientes.add(ingrediente)
                ing_cant[ingrediente] = cantidad

            ii+=1
            field_name = f'ingrediente_{ii}'
            field_cantidad = f'cantidad_{ii}'

        self.cleaned_data["ingredientes"] = ing_cant