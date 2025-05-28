from django import forms
from .models import Servicio

from django import forms
from .models import Servicio, TurnoHorario

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'turnos']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'turnos': forms.CheckboxSelectMultiple(),
        }
        help_texts = {
            'turnos': 'Selecciona en qué turnos se ofrece este servicio.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['turnos'].queryset = TurnoHorario.objects.all()