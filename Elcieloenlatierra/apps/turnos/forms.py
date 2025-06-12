from django import forms
from apps.turnos.models import Turno
from apps.servicios.models import Servicio
from django.contrib.auth.models import User
from apps.perfil.models import Perfil 
from datetime import time

class TurnoForm(forms.ModelForm):
    dni = forms.CharField(max_length=20, required=True, label="DNI del cliente")

    HORARIOS_POR_TURNO = {
        'mañana': ['07:00', '08:00', '09:00', '10:00', '11:00'],
        'tarde': ['13:00', '14:00', '15:00', '16:00', '17:00', '18:00'],
        'noche': ['19:00', '20:00', '21:00', '22:00'],
    }

    hora = forms.ChoiceField(choices=[])  # se rellena dinámicamente

    class Meta:
        model = Turno
        fields = ['servicio', 'fecha', 'turno', 'hora', 'notas']

        widgets = {
            'fecha': forms.TextInput(attrs={'class': 'flatpickr', 'autocomplete': 'off'}),
        }

    def __init__(self, *args, **kwargs):
        servicio_id = kwargs.pop('servicio_id', None)
        super().__init__(*args, **kwargs)

        servicio = None
        if servicio_id:
            try:
                servicio = Servicio.objects.get(id=servicio_id)
            except Servicio.DoesNotExist:
                servicio = None
        elif self.instance.pk:
            servicio = self.instance.servicio

        if servicio:
            turnos_del_servicio = servicio.turnos
            horas_disponibles = []
            for turno_nombre in turnos_del_servicio:
                horas_disponibles.extend(self.HORARIOS_POR_TURNO.get(turno_nombre, []))
            horas_disponibles = sorted(set(horas_disponibles))
            self.fields['hora'].choices = [(h, h) for h in horas_disponibles]
        else:
            self.fields['hora'].choices = []

        # Si la instancia tiene usuario, precargar el dni
        if self.instance and self.instance.pk and self.instance.usuario:
            perfil = getattr(self.instance.usuario, 'perfil', None)
            if perfil:
                self.fields['dni'].initial = perfil.dni

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        # Validar que exista un Perfil con ese DNI
        if not Perfil.objects.filter(dni=dni).exists():
            raise forms.ValidationError("No existe ningún usuario con ese DNI.")
        return dni

    def clean_hora(self):
        hora_str = self.cleaned_data['hora']
        try:
            hora_obj = time.fromisoformat(hora_str)
        except ValueError:
            raise forms.ValidationError("Hora inválida.")
        return hora_obj

    def save(self, commit=True):
        turno = super().save(commit=False)
        dni = self.cleaned_data.get('dni')

        # Obtener el usuario a partir del dni
        perfil = Perfil.objects.get(dni=dni)
        turno.usuario = perfil.user

        if commit:
            turno.save()
        return turno
