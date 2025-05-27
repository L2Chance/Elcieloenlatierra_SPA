from django import forms
from apps.servicios.models import Servicio
from .models import Turno

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['servicio', 'cliente_nombre', 'telefono', 'email', 'fecha', 'notas']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control flatpickr', 'autocomplete': 'off'}),
            'cliente_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'servicio': forms.Select(attrs={'class': 'form-select'}),
        }