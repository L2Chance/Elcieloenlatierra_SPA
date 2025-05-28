from django.db import models
from cloudinary.models import CloudinaryField

class TurnoHorario(models.Model):
    nombre = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = CloudinaryField('imagen')
    turnos = models.ManyToManyField(TurnoHorario, related_name="servicios", help_text="Selecciona en qué turnos se ofrece este servicio")

    def __str__(self):
        return self.nombre