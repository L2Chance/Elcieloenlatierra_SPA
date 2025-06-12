from django import forms
from apps.reservas.models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['servicio', 'fecha', 'turno', 'notas']
        widgets = {
            'fecha': forms.TextInput(attrs={'class': 'flatpickr', 'autocomplete': 'off'}),
            'notas': forms.Textarea(attrs={'rows': 3}),
        }
