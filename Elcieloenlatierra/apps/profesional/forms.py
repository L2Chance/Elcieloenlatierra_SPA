from django import forms
from .models import Profesional

class ProfesionalForm(forms.ModelForm):
    class Meta:
        model = Profesional
        fields = ['titulo', 'servicios', 'turnos']
        widgets = {
            'titulo': forms.Select(attrs={'class': 'form-control'}),
            'servicios': forms.CheckboxSelectMultiple(),
            'turnos': forms.CheckboxSelectMultiple(),
        }