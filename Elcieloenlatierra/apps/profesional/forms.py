from django import forms
from .models import Profesional
from apps.profesion.models import Profesion

class ProfesionalForm(forms.ModelForm):
    profesiones = forms.ModelMultipleChoiceField(
        queryset=Profesion.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Profesiones"
    )

    class Meta:
        model = Profesional
        fields = ['profesiones']

# forms.py
from django import forms
from .models import Profesional

class AprobacionProfesionalForm(forms.ModelForm):
    class Meta:
        model = Profesional
        fields = ['aprobado']