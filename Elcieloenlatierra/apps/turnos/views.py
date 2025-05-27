from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import TurnoForm
from django.contrib.auth.decorators import login_required

from .forms import TurnoForm

@login_required
def solicitud_turno(request):
    enviado = False

    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            turno = form.save(commit=False)
            turno.usuario = request.user  # 🔥 Asociar el turno con el usuario actual
            turno.save()
            enviado = True
            form = TurnoForm(initial={'email': request.user.email})
    else:
        form = TurnoForm(initial={'email': request.user.email})

    return render(request, 'turnos/formularios/solicitud_turno.html', {'form': form, 'enviado': enviado})
