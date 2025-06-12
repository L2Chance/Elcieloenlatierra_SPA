from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from apps.profesion.models import Profesion
from .forms import ProfesionalForm
from .models import Profesional
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .forms import AprobacionProfesionalForm
from .models import Profesional
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime
from django.utils import timezone
from apps.perfil.models import Perfil



from apps.turnos.models import Turno 
from apps.servicios.models import Servicio

@login_required
def registrar_profesional(request):
    try:
        profesional = Profesional.objects.get(user=request.user)
    except Profesional.DoesNotExist:
        profesional = None

    if request.method == 'POST':
        form = ProfesionalForm(request.POST, instance=profesional)
        if form.is_valid():
            profesional = form.save(commit=False)
            profesional.user = request.user
            profesional.save()
            form.save_m2m()  

            subject = "Nueva solicitud de profesional"
            message = (
                f"El usuario {request.user.get_full_name() or request.user.username} "
                f"ha enviado una solicitud para ser profesional.\n\n"
                f"Revisala en el panel de administración o desde la sección correspondiente del sitio."
            )
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [settings.DEFAULT_FROM_EMAIL]  
            send_mail(subject, message, from_email, to_email)

            messages.success(request, "Perfil profesional guardado correctamente. En breve será revisado.")
            return redirect('/perfil/detalle')  
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = ProfesionalForm(instance=profesional)

    return render(request, 'profesional/registro-profesional.html', {'form': form})

def aprobar_profesional(request, profesional_id):
    profesional = get_object_or_404(Profesional, id=profesional_id)

    if request.method == 'POST':
        form = AprobacionProfesionalForm(request.POST, instance=profesional)
        if form.is_valid():
            form.save()
            messages.success(request, "Profesional actualizado correctamente.")
            return redirect('listar_solicitudes_profesionales')
        else:
            messages.error(request, "Hubo un error al procesar el formulario.")
    else:
        form = AprobacionProfesionalForm(instance=profesional)

    return render(request, 'profesional/aprobar-profesional.html', {
        'form': form,
        'profesional': profesional
    })

def listar_solicitudes_profesionales(request):
    profesionales_pendientes = Profesional.objects.filter(aprobado=False)
    profesiones = Profesion.objects.all()
    return render(request, 'panel-de-control/panel_de_control.html', {
        'profesionales': profesionales_pendientes,
        'profesiones': profesiones,
    })

def aprobar_profesional(request, profesional_id):
    profesional = get_object_or_404(Profesional, id=profesional_id)
    profesional.aprobado = True
    profesional.save()
    messages.success(request, "Profesional aprobado correctamente.")
    return redirect('listar_solicitudes_profesionales')

@staff_member_required
def rechazar_profesional(request, profesional_id):
    profesional = get_object_or_404(Profesional, id=profesional_id)
    profesional.delete()
    messages.success(request, "Solicitud rechazada y eliminada.")
    return redirect('listar_solicitudes_profesionales')

@login_required
def mostrar_perfil_profesional(request):
    profesional = getattr(request.user, 'profesional', None)
    if not profesional:
        return redirect('home')

    fecha_str = request.GET.get('fecha')
    if fecha_str:
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            fecha = timezone.localdate()
    else:
        fecha = timezone.localdate()

    servicios = Servicio.objects.filter(profesiones__in=profesional.profesiones.all()).distinct()
    turnos = Turno.objects.filter(servicio__in=servicios, fecha=fecha).order_by('hora')

    dnis = [turno.dni for turno in turnos]
    perfiles = Perfil.objects.filter(dni__in=dnis)
    perfil_por_dni = {perfil.dni: f"{perfil.nombre} {perfil.apellido}" for perfil in perfiles}

    # Crear una lista de dicts con info del turno + nombre completo del cliente
    turnos_con_cliente = []
    for turno in turnos:
        nombre_cliente = perfil_por_dni.get(turno.dni, "Desconocido")
        turno_info = {
            'servicio': turno.servicio.nombre,
            'turno': turno.turno,
            'hora': turno.hora,
            'dni': turno.dni,
            'notas': turno.notas,
            'cliente': nombre_cliente,
        }
        turnos_con_cliente.append(turno_info)

    context = {
        'profesional': profesional,
        'turnos': turnos_con_cliente,
        'fecha_seleccionada': fecha,
    }
    return render(request, 'profesional/profesional_perfil.html', context)