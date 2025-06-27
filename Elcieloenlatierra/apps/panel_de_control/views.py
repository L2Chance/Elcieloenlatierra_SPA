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
from apps.roles.forms import CrearRolForm
from django.contrib.auth.models import User 
from django.contrib.auth.models import Group 


def asignar_rol(request):
    usuarios = User.objects.all()

    for usuario in usuarios:
        rol_id = request.POST.get(f'rol_{usuario.id}')
        if rol_id is not None:
            usuario.groups.clear()
            if rol_id != "":
                try:
                    nuevo_rol = Group.objects.get(id=rol_id)
                    usuario.groups.add(nuevo_rol)
                except Group.DoesNotExist:
                    continue  # ignorar si no existe el rol

    messages.success(request, "Roles actualizados correctamente.")
    return redirect('panel_control')

def mostrar_panel_de_control(request):
    servicios = Servicio.objects.all()
    profesiones = Profesion.objects.all()
    profesionales_pendientes = Profesional.objects.filter(aprobado=False)
    profesionales_aprobados = Profesional.objects.filter(aprobado=True)
    usuarios = User.objects.all()
    roles = Group.objects.all()


 # Agrega esta parte para calcular cantidad de turnos y ganancias por servicio
    ganancias_por_servicio = Servicio.objects.annotate(
        cantidad_turnos=Count('turnos_turno'),
        total_ganado=ExpressionWrapper(
            F('precio') * Count('turnos_turno'),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )

    if request.method == "POST" and "crear_rol_submit" in request.POST:
            rol_form = CrearRolForm(request.POST)
            if rol_form.is_valid():
                # guardar rol
                ...
                return redirect('panel_control')
    else:
        rol_form = CrearRolForm()

    servicio_form = ServicioForm()
    profesion_form = ProfesionForm()

    context = {
        'servicios': servicios,
        'profesiones': profesiones,
        'profesionales': profesionales_pendientes,
        'profesionales_aprobados': profesionales_aprobados,
        'servicio_form': servicio_form,
        'profesion_form': profesion_form,
        'rol_form': rol_form,
        'ganancias_por_servicio': ganancias_por_servicio,
        'usuarios': usuarios,
        'roles': roles,
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

from django.contrib.auth.models import Group
from apps.roles.forms import CrearRolForm 

def crear_rol(request):
    if request.method == 'POST':
        form = CrearRolForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            permisos = form.cleaned_data['permisos']

            if Group.objects.filter(name=nombre).exists():
                messages.error(request, 'Ya existe un rol con ese nombre.')
            else:
                grupo = Group.objects.create(name=nombre)
                grupo.permissions.set(permisos)
                grupo.save()
                messages.success(request, 'Rol creado exitosamente.')
        else:
            messages.error(request, 'Por favor, corregí los errores del formulario.')

    return redirect('panel_control')

@staff_member_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)

    if request.method == "POST":
        usuario.delete()
        messages.success(request, "Usuario eliminado correctamente.")
    
    return redirect('panel_control')