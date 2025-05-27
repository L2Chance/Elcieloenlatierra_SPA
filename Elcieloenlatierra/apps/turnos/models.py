from django.db import models
from apps.servicios.models import Servicio
from django.core.validators import RegexValidator

from django.contrib.auth.models import User

class Turno(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='turnos', null=True)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='turnos')
    cliente_nombre = models.CharField(max_length=100)
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="El número debe ingresarse en formato: '+999999999'. Hasta 15 dígitos permitidos."
        )]
    )
    email = models.EmailField(blank=True, null=True)
    fecha = models.DateField()
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Turno de {self.usuario.username} para {self.servicio.nombre} el {self.fecha}"