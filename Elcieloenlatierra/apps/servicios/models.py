from django.db import models
from cloudinary.models import CloudinaryField

class Servicio(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = CloudinaryField('imagen')
    periodo = models.CharField(max_length=100, help_text="Ej: 20-30 Min")

    def __str__(self):
        return self.titulo