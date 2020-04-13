from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class FormRegistro(UserCreationForm):
    nombre = forms.CharField(max_length=30, required=False, help_text='Optional.')
    apellidos = forms.CharField(max_length=64, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Requerido')
    claveMaestra = forms.CharField(max_length=24, help_text='Clave obligatoria prefijada')

    class Meta:
        model = User
        fields = ('username', 'nombre', 'apellidos', 'email', 'password1', 'password2', 'claveMaestra')