from django.db import models
from apps.servicios.models import Servicio
from django.contrib.auth.models import User

def obtener_usuario_por_defecto():
    return User.objects.first().pk

TURNOS_CHOICES = [
    ('mañana', 'Turno Mañana'),
    ('tarde', 'Turno Tarde'),
    ('noche', 'Turno Noche'),
]

class Reserva(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='reservas_reserva')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=obtener_usuario_por_defecto)
    fecha = models.DateField()
    turno = models.CharField(max_length=10, choices=TURNOS_CHOICES)
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reserva de {self.usuario.username} para {self.servicio.nombre} el {self.fecha} en el turno {self.turno}"
