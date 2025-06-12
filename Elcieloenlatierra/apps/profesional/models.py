from django.db import models
from django.contrib.auth.models import User
from apps.profesion.models import Profesion 

class Profesional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profesiones = models.ManyToManyField(Profesion, blank=True)
    aprobado = models.BooleanField(default=False)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        perfil = getattr(self.user, 'perfil', None)
        profesiones_nombres = ", ".join([p.nombre for p in self.profesiones.all()]) or "Sin Profesión"
        if perfil:
            return f"{profesiones_nombres} - {perfil.nombre} {perfil.apellido}"
        return f"{profesiones_nombres} - {self.user.username}"