from django.db import models
from django.contrib.auth.models import User

class Profesional(models.Model):
    TITULOS = [
        ('TER', 'Terapeuta'),
        ('MAS', 'Masajista'),
        ('EST', 'Esteticista'),
        ('COS', 'Cosmetóloga'),
        ('MAN', 'Manicurista'),
        ('PED', 'Pedicurista'),
        ('DEP', 'Especialista en Depilación'),
        ('FAC', 'Facialista'),
        ('SPA', 'Especialista en Spa'),
        ('OTR', 'Otro'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=3, choices=TITULOS)
    servicios = models.ManyToManyField('servicios.Servicio', blank=True)
    aprobado = models.BooleanField(default=False)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    turnos = models.ManyToManyField(
        'servicios.TurnoHorario',
        related_name='profesionales',
        blank=True,
        help_text="Selecciona en qué turnos trabaja este profesional"
    )

    def __str__(self):
        perfil = getattr(self.user, 'perfil', None)
        if perfil:
            return f"{self.get_titulo_display()} - {perfil.nombre} {perfil.apellido}"
        return f"{self.get_titulo_display()} - {self.user.username}"