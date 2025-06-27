from django import forms
from .models import Perfil
from apps.profesion.models import Profesion

class PerfilForm(forms.ModelForm):
    profesion = forms.ModelChoiceField(
        queryset=Profesion.objects.all(),
        required=False,
        empty_label="Seleccioná una profesión",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Perfil
        fields = ['nombre', 'apellido', 'dni', 'genero', 'telefono', 'foto_perfil', 'profesion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_perfil': forms.FileInput(attrs={
                'style': 'display:none;',
                'id': 'id_foto_perfil'
            }),
            # ❌ Ya no necesitás definir el widget de 'profesion' acá
        }