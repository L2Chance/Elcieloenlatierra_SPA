from datetime import date
from django.shortcuts import render, redirect
from apps.perfil.forms import PerfilForm
from django.contrib.auth.decorators import login_required

from apps.turnos.models import Turno

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
            return redirect('detalle_perfil')  
    else:
        form = PerfilForm()

    return render(request, 'perfil/crear_perfil.html', {'form': form})

@login_required
def crear_primer_perfil(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'perfil/crear_perfil.html', {'form': form})

@login_required
def editar_perfil(request):
    perfil = request.user.perfil
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('detalle_perfil')
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
    hoy = date.today()

    dni_usuario = request.user.perfil.dni
    turnos_todos = Turno.objects.filter(dni=dni_usuario).order_by('fecha', 'hora')
    turnos_proximos = turnos_todos.filter(fecha__gte=hoy)

    contexto = {
        'perfil': perfil,
        'email': request.user.email,
        'turnos_todos': turnos_todos,
        'turnos_proximos': turnos_proximos,
        'today': hoy,
    }
    return render(request, 'perfil/detalle_perfil.html', contexto)