from django import forms
from .models import Perfil

class PerfilForm(forms.ModelForm):
    foto_perfil = forms.ClearableFileInput()

    class Meta:
        model = Perfil
        fields = ['nombre', 'apellido', 'dni', 'genero', 'telefono', 'foto_perfil']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_perfil': forms.ClearableFileInput(attrs={'style': 'display:none;', 'id': 'id_foto_perfil'}),
        }