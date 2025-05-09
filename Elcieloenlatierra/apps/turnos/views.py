from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import TurnoForm
from django.contrib.auth.decorators import login_required

@login_required
def solicitud_turno(request):
    enviado = False
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data

            asunto = "Nueva solicitud de turno"
            mensaje = (
                f"📅 Solicitud de turno recibida:\n\n"
                f"Nombre: {datos['nombre']}\n"
                f"Correo: {datos['email']}\n"
                f"Teléfono: {datos['telefono']}\n"
                f"Fecha: {datos['fecha']}\n"
                f"Horario: {datos['horario']}\n"
                f"Servicio: {datos['servicio']}\n"
                f"Comentarios: {datos['comentarios']}\n\n"
                f"✅ Fin del mensaje."
            )

            destinatarios = ['elcieloenlatierraspa@gmail.com']  

     
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                destinatarios,
                fail_silently=False,
            )

            enviado = True
            form = TurnoForm()
    else:
        form = TurnoForm()

    return render(request, 'turnos/formularios/solicitud_turno.html', {
        'form': form,
        'enviado': enviado
    })
