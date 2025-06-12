from django import forms
from .models import Profesion

class ProfesionForm(forms.ModelForm):
    class Meta:
        model = Profesion
        fields = ['nombre', 'servicios']
        widgets = {
            'servicios': forms.CheckboxSelectMultiple(),  # o forms.SelectMultiple() si preferís un dropdown múltiple
        }
        labels = {
            'nombre': 'Nombre de la profesión',
            'servicios': 'Servicios ofrecidos',
        }