from django.shortcuts import render
from apps.perfil.forms import PerfilForm

def editar_perfil(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save() 
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'perfil/modificar_perfil.html', {'form': form})

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Perfil

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)