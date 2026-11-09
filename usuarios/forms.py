from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group
from django.db import transaction

from .models import Usuario
from .roles import GRUPO_CLIENTES


class RegistroForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico', required=True)

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {'first_name': 'Nombre', 'last_name': 'Apellido'}

    @transaction.atomic
    def guardar_cliente(self):
        usuario = self.save()
        grupo, _ = Group.objects.get_or_create(name=GRUPO_CLIENTES)
        usuario.groups.add(grupo)
        return usuario


class IngresoForm(AuthenticationForm):
    username = forms.CharField(label='Usuario', widget=forms.TextInput(
        attrs={'autofocus': True, 'autocomplete': 'username'},
    ))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password'},
    ))
