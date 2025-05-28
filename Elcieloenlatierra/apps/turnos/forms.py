from django import forms
from .models import Turno
import datetime

# Horarios disponibles por turno
HORARIOS = {
    'manana': [(datetime.time(h, 0), f'{h:02d}:00') for h in range(7, 12)],
    'tarde': [(datetime.time(h, 0), f'{h:02d}:00') for h in range(14, 19)],
    'noche': [(datetime.time(h, 0), f'{h:02d}:00') for h in range(19, 22)],
}

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['servicio', 'fecha', 'turno', 'hora', 'notas']
        widgets = {
            'fecha': forms.DateInput(attrs={
                'class': 'form-control flatpickr',
                'autocomplete': 'off'
            }),
            'turno': forms.Select(attrs={
                'class': 'form-select',
                'id': 'turno-select'
            }),
            'hora': forms.Select(attrs={
                'class': 'form-select',
                'id': 'hora-select'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'servicio': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Por defecto, mostrar las horas del turno mañana
        self.fields['hora'].choices = HORARIOS['manana']