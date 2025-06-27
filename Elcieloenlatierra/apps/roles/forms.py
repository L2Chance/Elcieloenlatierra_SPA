# roles/forms.py
from django import forms
from django.contrib.auth.models import Permission

class CrearRolForm(forms.Form):
    nombre = forms.CharField(label="Nombre del Rol", max_length=150)
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all().select_related('content_type'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Permisos"
    )