from django.db import models
from apps.servicios.models import Servicio
from django.contrib.auth.models import User

TURNOS_CHOICES = [
    ('mañana', 'Turno Mañana'),
    ('tarde', 'Turno Tarde'),
    ('noche', 'Turno Noche'),
]

class Turno(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='turnos_turno')
    profesional = models.ForeignKey(User, on_delete=models.CASCADE, related_name='turnos_asignados', null=True,
    blank=True)
    dni = models.CharField(max_length=20, default='00000000')
    fecha = models.DateField()
    turno = models.CharField(max_length=10, choices=TURNOS_CHOICES)
    hora = models.TimeField()
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Turno para DNI {self.dni} - {self.servicio.nombre} el {self.fecha} a las {self.hora}"