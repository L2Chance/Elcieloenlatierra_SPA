from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.core.validators import RegexValidator

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    dni = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(
        max_length=20,
        null=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="El número debe ingresarse en formato: '+999999999'. Hasta 15 dígitos permitidos."
        )]
    )
    foto_perfil = CloudinaryField(
        'foto de perfil',
        blank=True,
        null=True,
        default='predeterminated_r7bawf'
    )
    GENERO_OPCIONES = [
        ('ND', 'No definido'),
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

    # 🔹 NUEVO CAMPO AGREGADO
    profesion = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        default="No tiene",
        help_text="Profesión del usuario si es profesional"
    )

    @property
    def fecha_registro(self):
        return self.user.date_joined

    def __str__(self):
        return f"{self.user.username} - Perfil"

    @property
    def primer_nombre(self):
        return self.nombre.split(' ')[0] if self.nombre else ''


