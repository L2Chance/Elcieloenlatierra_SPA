import datetime
from django.db import models
from cloudinary.models import CloudinaryField

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = CloudinaryField('imagen')
    periodo = models.CharField(max_length=100, help_text="Ej: 20-30 Min")
    hora = models.TimeField(
        help_text="Hora de inicio en que se ofrece el servicio",
        default=datetime.time(10, 0)
    )

    def __str__(self):
        return self.nombre