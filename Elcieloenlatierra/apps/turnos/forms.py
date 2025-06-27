from django import forms
from django.contrib.auth.models import User
from .models import Turno, Servicio
from datetime import time
from apps.perfil.models import Perfil
from django.forms import HiddenInput

class ProfesionalModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        perfil = getattr(obj, 'perfil', None)
        if perfil:
            # Retornás nombre + apellido
            return f"{perfil.nombre} {perfil.apellido}"
        return obj.username

class TurnoForm(forms.ModelForm):
    dni = forms.CharField(max_length=20, required=True, label="DNI del cliente")

    profesional = ProfesionalModelChoiceField(
        queryset=User.objects.filter(groups__name='Profesional').select_related('perfil'),
        required=True,
        label="Profesional",
        widget=HiddenInput())

    HORARIOS_POR_TURNO = {
        'mañana': ['07:00', '08:00', '09:00', '10:00', '11:00'],
        'tarde': ['13:00', '14:00', '15:00', '16:00', '17:00', '18:00'],
        'noche': ['19:00', '20:00', '21:00', '22:00'],
    }

    hora = forms.ChoiceField(choices=[])

    class Meta:
        model = Turno
        fields = ['servicio', 'profesional', 'fecha', 'turno', 'hora', 'notas']

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

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
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

        # Asociar cliente según el DNI
        perfil = Perfil.objects.get(dni=dni)
        turno.dni = dni  # actualizar por si cambia en el form
        turno.profesional = self.cleaned_data['profesional']

        if commit:
            turno.save()
        return turno
