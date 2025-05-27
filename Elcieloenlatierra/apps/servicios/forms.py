from django import forms
from .models import Servicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'periodo', 'hora']
        widgets = {
            'hora': forms.TimeInput(attrs={
                'class': 'form-control flatpickr-hour',
                'autocomplete': 'off'
            }),
        }