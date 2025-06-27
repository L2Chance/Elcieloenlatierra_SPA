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
from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML



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
def exportar_turnos_pdf(request):
    user = request.user

    # Verificar grupo Profesional
    if not user.groups.filter(name='Profesional').exists():
        return redirect('home')

    dni_filtro = request.GET.get('dni', '').strip()
    fecha_str = request.GET.get('fecha', '').strip()

    queryset = Turno.objects.filter(profesional=user).order_by('fecha', 'hora')

    # Filtrar por DNI si se proporciona
    if dni_filtro:
        queryset = queryset.filter(dni=dni_filtro)

    # Filtrar por fecha si se proporciona y no hay DNI
    fecha = None
    if fecha_str and not dni_filtro:
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            queryset = queryset.filter(fecha=fecha)
        except ValueError:
            fecha = timezone.localdate()
            queryset = queryset.filter(fecha=fecha)
    elif not fecha_str and not dni_filtro:
        fecha = timezone.localdate()
        queryset = queryset.filter(fecha=fecha)

    # Si hay DNI filtrado, ignorar filtro de fecha para mostrar todos los turnos de ese DNI
    if dni_filtro:
        fecha = None

    # Obtener perfiles de clientes según DNIs en queryset
    dnis = queryset.values_list('dni', flat=True).distinct()
    perfiles = Perfil.objects.filter(dni__in=dnis)
    perfil_por_dni = {perfil.dni: f"{perfil.nombre} {perfil.apellido}" for perfil in perfiles}

    turnos_con_cliente = []
    for turno in queryset:
        nombre_cliente = perfil_por_dni.get(turno.dni, "Desconocido")
        turnos_con_cliente.append({
            'servicio': turno.servicio.nombre,
            'turno': turno.turno,
            'hora': turno.hora,
            'dni': turno.dni,
            'notas': turno.notas,
            'cliente': nombre_cliente,
            'fecha': turno.fecha,
        })

    template = get_template('profesional/pdf_turnos.html')
    html_string = template.render({
        'profesional': user,
        'fecha': fecha,
        'dni_filtrado': dni_filtro,
        'turnos': turnos_con_cliente,
    })

    pdf = HTML(string=html_string).write_pdf()

    filename = "turnos"
    if dni_filtro:
        filename += f"_dni_{dni_filtro}"
    if fecha:
        filename += f"_{fecha}"
    filename += ".pdf"

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename={filename}'
    return response



def mostrar_perfil_profesional(request):
    user = request.user

    # Verificar si el usuario pertenece al grupo "Profesional"
    if not user.groups.filter(name='Profesional').exists():
        return redirect('home')

    dni_filtro = request.GET.get('dni', '').strip()
    fecha_str = request.GET.get('fecha', '').strip()

    # Inicializamos queryset base de turnos del profesional actual
    queryset = Turno.objects.filter(profesional=user).order_by('fecha', 'hora')

    # Filtrar por DNI si se proporciona
    if dni_filtro:
        queryset = queryset.filter(dni=dni_filtro)

    # Filtrar por fecha si se proporciona y no hay DNI
    fecha = None
    if fecha_str and not dni_filtro:
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            queryset = queryset.filter(fecha=fecha)
        except ValueError:
            fecha = timezone.localdate()
            queryset = queryset.filter(fecha=fecha)
    elif not fecha_str and not dni_filtro:
        # Si no hay filtro, mostrar solo turnos de hoy
        fecha = timezone.localdate()
        queryset = queryset.filter(fecha=fecha)

    # Si hay DNI filtrado, ignorar filtro de fecha para mostrar todos los turnos de ese DNI
    if dni_filtro:
        fecha = None  # para que en la plantilla puedas saber que no se filtró por fecha

    # Obtener los perfiles de clientes para los DNIs en turnos
    dnis = queryset.values_list('dni', flat=True).distinct()
    perfiles = Perfil.objects.filter(dni__in=dnis)
    perfil_por_dni = {perfil.dni: f"{perfil.nombre} {perfil.apellido}" for perfil in perfiles}

    # Preparar lista de turnos para la plantilla
    turnos_con_cliente = []
    for turno in queryset:
        nombre_cliente = perfil_por_dni.get(turno.dni, "Desconocido")
        turnos_con_cliente.append({
            'servicio': turno.servicio.nombre,
            'turno': turno.turno,
            'hora': turno.hora,
            'dni': turno.dni,
            'notas': turno.notas,
            'cliente': nombre_cliente,
            'fecha': turno.fecha,
        })

    context = {
        'profesional': user,
        'turnos': turnos_con_cliente,
        'fecha_seleccionada': fecha,
        'dni_filtrado': dni_filtro,
    }
    return render(request, 'profesional/profesional_perfil.html', context)