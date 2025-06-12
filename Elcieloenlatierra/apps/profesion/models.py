from django.db import models
from apps.servicios.models import Servicio

class Profesion(models.Model):
    nombre = models.CharField("Nombre de la profesión", max_length=100, unique=True)
    servicios = models.ManyToManyField(Servicio, related_name="profesiones", blank=True)

    def __str__(self):
        return self.nombre