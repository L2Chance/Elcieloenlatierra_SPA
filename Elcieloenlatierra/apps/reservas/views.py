from django.forms import modelformset_factory
from django.shortcuts import render
from apps.reservas.models import Reserva
from apps.servicios.models import Servicio
from .forms import ReservaForm 
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def reservar_turno(request):
    servicios = Servicio.objects.all()
    servicios_turnos = {servicio.id: servicio.turnos for servicio in servicios}

    ReservaFormSet = modelformset_factory(
        Reserva,          # Acá va el modelo correcto
        form=ReservaForm,
        extra=1,
        can_delete=True,
    )

    if request.method == 'POST':
        formset = ReservaFormSet(request.POST, queryset=Reserva.objects.none())  # Acá también

        if formset.is_valid():
            for form in formset:
                reserva = form.save(commit=False)
                reserva.usuario = request.user
                reserva.save()
            enviado = True
            formset = ReservaFormSet(queryset=Reserva.objects.none())
        else:
            enviado = False
    else:
        formset = ReservaFormSet(queryset=Reserva.objects.none())
        enviado = False

    context = {
        'formset': formset,
        'enviado': enviado,
        'servicios': servicios,
        'servicios_turnos_json': json.dumps(servicios_turnos, cls=DjangoJSONEncoder),
    }

    return render(request, 'reservas/formulario-reservas.html', context)

@login_required
def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id, usuario=request.user)

    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "Reserva cancelada correctamente.")
        return redirect('vista_donde_listas_reservas')
    
    messages.error(request, "Método no permitido.")
    return redirect('vista_donde_listas_reservas')