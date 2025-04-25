from django import forms
from apps.servicios.models import Servicio 

from datetime import time, timedelta, datetime

def generar_horarios():
    horarios = []
    hora_actual = datetime.strptime("07:00", "%H:%M")
    fin = datetime.strptime("21:00", "%H:%M")
    while hora_actual <= fin:
        hora_str = hora_actual.strftime("%H:%M")
        horarios.append((hora_str, hora_str))
        hora_actual += timedelta(minutes=30)
    return horarios

class TurnoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    telefono = forms.CharField(max_length=20)
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    horario = forms.ChoiceField(choices=generar_horarios(), label="Horario")
    servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.all(),
        empty_label="Seleccioná un servicio"
    )
    comentarios = forms.CharField(widget=forms.Textarea, required=False)