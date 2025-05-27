from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30, blank=True)
    apellido = models.CharField(max_length=30, blank=True)
    dni = models.CharField(max_length=20, unique=True)
    foto_perfil = CloudinaryField(
        'foto de perfil',
        blank=True,
        null=True,
        default='predeterminated_r7bawf'
    )

    def __str__(self):
        return f"{self.user.username} - Perfil"