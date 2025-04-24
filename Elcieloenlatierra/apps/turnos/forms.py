from django import forms
from apps.servicios.models import Servicio 

class TurnoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()
    telefono = forms.CharField(max_length=20)
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.all(),
        empty_label="Seleccioná un servicio"
    )
    comentarios = forms.CharField(widget=forms.Textarea, required=False)