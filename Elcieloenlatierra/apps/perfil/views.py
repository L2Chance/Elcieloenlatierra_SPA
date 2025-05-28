from django.shortcuts import render, redirect
from apps.perfil.forms import PerfilForm
from django.contrib.auth.decorators import login_required

@login_required
def crear_perfil(request):
    try:
        # Si el perfil ya existe, redirigimos o mostramos el formulario para editar
        perfil = request.user.perfil
        return redirect('editar_perfil')  # O donde quieras
    except Perfil.DoesNotExist:
        perfil = None

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            nuevo_perfil = form.save(commit=False)
            nuevo_perfil.user = request.user
            nuevo_perfil.save()
            return redirect('detalle_perfil')  # Después de crear perfil redirigimos a la vista detalle
    else:
        form = PerfilForm()

    return render(request, 'perfil/crear_perfil.html', {'form': form})

@login_required
def editar_perfil(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('detalle_perfil')  # Cambiá esto por el nombre de tu vista de detalle
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'perfil/modificar_perfil.html', {'form': form})


def crear_perfil(request):

    return 

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Perfil

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

@login_required
def detalle_perfil(request):
    perfil = request.user.perfil
    contexto = {
        'perfil': perfil,
        'email': request.user.email,
    }
    return render(request, 'perfil/detalle_perfil.html', contexto)