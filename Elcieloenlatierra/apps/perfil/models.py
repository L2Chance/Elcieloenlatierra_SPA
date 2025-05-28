from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.core.validators import RegexValidator

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #Obligatorio
    nombre = models.CharField(max_length=30) #Obligatorio
    apellido = models.CharField(max_length=30) #Obligatorio
    dni = models.CharField(max_length=20, unique=True) #Obligatorio
    telefono = models.CharField(
        max_length=20,
        null=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="El número debe ingresarse en formato: '+999999999'. Hasta 15 dígitos permitidos."
        )] #Opcional
    )
    foto_perfil = CloudinaryField(
        'foto de perfil',
        blank=True,
        null=True,
        default='predeterminated_r7bawf' #Opcional
    )
    GENERO_OPCIONES = [
    ('ND', 'No definido'),  # opción por defecto
    ('F', 'Femenino'),
    ('M', 'Masculino'),
]

    genero = models.CharField(
        max_length=2,
        choices=GENERO_OPCIONES,
        default='ND',
        blank=True,
        null=True,
    )

    @property
    def fecha_registro(self):
        return self.user.date_joined #Obligatorio

    def __str__(self):
        return f"{self.user.username} - Perfil"
