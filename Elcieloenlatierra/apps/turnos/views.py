from pyexpat.errors import messages
from django.core.mail import send_mail
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date  # o from django.utils import timezone
from apps.turnos.models import Turno
from apps.servicios.models import Servicio
from apps.turnos.models import Turno
from .forms import TurnoForm
from django.contrib.auth.decorators import login_required
from apps.perfil.models import Perfil
from apps.reservas.models import Reserva


from .forms import TurnoForm

from django.contrib.auth.decorators import login_required
from apps.reservas.models import Reserva  # ajusta la ruta si es diferente

@login_required
def solicitud_turno(request):
    servicios = Servicio.objects.all()
    servicios_turnos = {servicio.id: servicio.turnos for servicio in servicios}

    TurnoFormSet = modelformset_factory(
        Turno,
        form=TurnoForm,
        extra=1,
        can_delete=True,
    )

    if request.method == 'POST':
        formset = TurnoFormSet(request.POST, queryset=Turno.objects.none())
        for form in formset.forms:
            servicio_id = form.data.get(f'{form.prefix}-servicio')
            if servicio_id:
                form.__init__(form.data, servicio_id=servicio_id)

        if formset.is_valid():
            for form in formset:
                turno = form.save(commit=False)
                turno.usuario = request.user  # Ojo que Turno no tiene usuario, quizá quitar esta línea
                turno.save()
            enviado = True
            formset = TurnoFormSet(queryset=Turno.objects.none())
        else:
            enviado = False
    else:
        formset = TurnoFormSet(queryset=Turno.objects.none())
        enviado = False

    # Obtener las reservas, con select_related para optimizar acceso a perfil
    reservas = Reserva.objects.select_related('usuario__perfil', 'servicio').order_by('-fecha', '-turno')[:20]

    context = {
        'formset': formset,
        'enviado': enviado,
        'servicios': servicios,
        'servicios_turnos': servicios_turnos,
        'reservas': reservas,
    }

    return render(request, 'turnos/formularios/solicitud_turno.html', context)


@login_required
def cancelar_turno(request, turno_id):
    if request.method == 'POST':
        usuario_dni = request.user.perfil.dni 
        turno = get_object_or_404(Turno, id=turno_id, dni=usuario_dni)

        if turno.fecha >= date.today():
            turno.delete()
            messages.success(request, "Turno cancelado correctamente.")
        else:
            messages.error(request, "No se pueden cancelar turnos pasados.")
    else:
        messages.error(request, "Método no permitido.")
    
    return redirect('detalle_perfil')