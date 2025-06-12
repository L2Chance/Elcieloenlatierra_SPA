from django.db import models
from cloudinary.models import CloudinaryField
from multiselectfield import MultiSelectField

TURNOS_DISPONIBLES = [
    ('mañana', 'Turno Mañana'),
    ('tarde', 'Turno Tarde'),
    ('noche', 'Turno Noche'),
]

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    imagen = CloudinaryField('imagen')
    turnos = MultiSelectField(
        choices=TURNOS_DISPONIBLES,
        max_length=20,
        default=['mañana', 'tarde', 'noche'] 
    )

    def __str__(self):
        return self.nombre