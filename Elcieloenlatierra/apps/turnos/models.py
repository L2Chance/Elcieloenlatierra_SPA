import datetime
from django.db import models
from apps.servicios.models import Servicio
from django.contrib.auth.models import User

class Turno(models.Model):
    TURNOS_CHOICES = [
        ('manana', 'Mañana'),
        ('tarde', 'Tarde'),
        ('noche', 'Noche'),
    ]
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='turnos_turno')
    fecha = models.DateField()
    turno = models.CharField(max_length=10, choices=TURNOS_CHOICES, default='manana')
    hora = models.TimeField(default=datetime.time(7, 0))
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Turno de {self.usuario.username} para {self.servicio.nombre} el {self.fecha} a las {self.hora}"