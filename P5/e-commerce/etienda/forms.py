from django import forms
from .models import obtenerCategoriasEleccion
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_starts_with_uppercase(value):
    if not value[0].isupper():
        raise ValidationError(
            _("Invalid.")
        )


class ProductoFormulario(forms.Form):
    nombre = forms.CharField(
        label='Name(*)',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'shadow border rounded w-full mb-4'}),
        validators=[validate_starts_with_uppercase]
    )

    precio = forms.DecimalField(
        label='Price(*)',
        widget=forms.TextInput(attrs={'class': 'shadow border rounded w-full mb-4'})
    )
    descripcion = forms.CharField(
        label='Description(*)',
        widget=forms.Textarea(attrs={'class': 'shadow border rounded w-full mb-4', 'rows': 4})
    )
    categoria = forms.ChoiceField(
        label='Category(*)',
        choices=obtenerCategoriasEleccion(),    # Así, si introduzco una nueva categoría, aparece al estar en la BD y no debo incluirla a mano. Hay que reiniciar el 'docker compose up' para que se vean las nuevas categorías
        widget=forms.Select(attrs={'class': 'block w-full py-2 px-3 border border-gray-300 bg-white rounded text-gray-700 leading-tight focus:outline-none focus:shadow-outline mb-4'}),
        required = False   # Aunque siempre se introduzca, va a estar vacío si se mete nueva categoría
    )
    nueva_categoria = forms.CharField(
        label='New category? Introduce to storage it',
        required=False,
        widget=forms.TextInput(attrs={'class': 'shadow border rounded w-full mb-4'})
    )
    imagen = forms.ImageField(
        label='Image(*)',
        #required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'shadow border rounded w-full mb-4'}),
        #upload_to='/imagenes'
    )


class LoginFormulario(forms.Form):
    username = forms.CharField(
        label='Name',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'shadow border rounded w-full mb-4'}),
        #validators=[validate_starts_with_uppercase]
    )

    contrasenia = forms.CharField(
        label='Password',
        max_length=100,
        widget=forms.PasswordInput(attrs={'class': 'shadow border rounded w-full mb-4'}),

    )