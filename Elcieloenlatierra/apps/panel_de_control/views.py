from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from apps.profesional.models import Profesional
from apps.servicios.models import Servicio
from apps.profesion.models import Profesion
from apps.servicios.forms import ServicioForm
from apps.profesion.forms import ProfesionForm
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from apps.profesional.models import Profesional
from django.core.mail import send_mail
from django.db.models import Count, F, ExpressionWrapper, DecimalField
from apps.turnos.models import Turno


def mostrar_panel_de_control(request):
    servicios = Servicio.objects.all()
    profesiones = Profesion.objects.all()
    profesionales_pendientes = Profesional.objects.filter(aprobado=False)
    profesionales_aprobados = Profesional.objects.filter(aprobado=True)

 # Agrega esta parte para calcular cantidad de turnos y ganancias por servicio
    ganancias_por_servicio = Servicio.objects.annotate(
        cantidad_turnos=Count('turnos_turno'),
        total_ganado=ExpressionWrapper(
            F('precio') * Count('turnos_turno'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )

    servicio_form = ServicioForm()
    profesion_form = ProfesionForm()

    context = {
        'servicios': servicios,
        'profesiones': profesiones,
        'profesionales': profesionales_pendientes,
        'profesionales_aprobados': profesionales_aprobados,
        'servicio_form': servicio_form,
        'profesion_form': profesion_form,
        'ganancias_por_servicio': ganancias_por_servicio,
    }

    return render(request, 'panel-de-control/panel_de_control.html', context)

# views.py

def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return redirect('panel_control')

def editar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('panel_control')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'panel-de-control/editar_servicio.html', {'form': form})

def eliminar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    servicio.delete()
    return redirect('panel_control')

def crear_profesion(request):
    if request.method == 'POST':
        form = ProfesionForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('panel_control')

def editar_profesion(request, pk):
    profesion = get_object_or_404(Profesion, pk=pk)
    if request.method == 'POST':
        form = ProfesionForm(request.POST, instance=profesion)
        if form.is_valid():
            form.save()
            return redirect('panel_control')
    else:
        form = ProfesionForm(instance=profesion)
    return render(request, 'profesional/editar_profesion.html', {'form': form})

def eliminar_profesion(request, pk):
    profesion = get_object_or_404(Profesion, pk=pk)
    profesion.delete()
    return redirect('panel_control')

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def aprobar_profesional(request, profesional_id):
    profesional = get_object_or_404(Profesional, id=profesional_id)
    profesional.aprobado = True
    profesional.save()

    # Enviar correo
    usuario = profesional.user
    send_mail(
        subject="Tu solicitud fue aprobada",
        message=(
            f"Hola {usuario.perfil.primer_nombre or usuario.username},\n\n"
            "Tu solicitud para ser profesional ha sido aprobada. Ya podés acceder con tu cuenta y comenzar a usar el sistema como profesional.\n\n"
            "¡Bienvenido a Sentirse Bien SPA!"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[usuario.email],
        fail_silently=True,
    )

    messages.success(request, "Profesional aprobado correctamente y notificado por correo.")
    return redirect('panel_control')

@staff_member_required
def rechazar_profesional(request, profesional_id):
    profesional = get_object_or_404(Profesional, id=profesional_id)
    usuario = profesional.user  # Guardar antes de borrar
    email = usuario.email

    # Enviar correo
    send_mail(
        subject="Tu solicitud fue rechazada",
        message=(
            f"Hola {usuario.perfil.primer_nombre or usuario.username},\n\n"
            "Lamentablemente, tu solicitud para ser profesional fue rechazada. "
            "Si creés que esto fue un error o necesitás más información, podés responder a este correo.\n\n"
            "Saludos."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=True,
    )

    profesional.delete()
    messages.success(request, "Solicitud rechazada, eliminada y notificada por correo.")
    return redirect('panel_control') 

def eliminar_profesional(request, profesional_id):
    profesional = get_object_or_404(Profesional, id=profesional_id)
    profesional.delete()
    messages.success(request, "Profesional eliminado correctamente.")
    return redirect('panel_control')