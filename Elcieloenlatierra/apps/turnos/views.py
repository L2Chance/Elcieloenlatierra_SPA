from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import TurnoForm

def solicitud_turno(request):
    enviado = False
    if request.method == 'POST':
        form = TurnoForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            print("📅 Solicitud de turno recibida:")
            print(f"Nombre: {datos['nombre']}")
            print(f"Correo: {datos['email']}")
            print(f"Teléfono: {datos['telefono']}")
            print(f"Fecha: {datos['fecha']}")
            print(f"Servicio: {datos['servicio']}")
            print(f"Comentarios: {datos['comentarios']}")
            print("✅ Fin del mensaje.\n")
            enviado = True
            form = TurnoForm()
    else:
        form = TurnoForm()

    return render(request, 'turnos/formularios/solicitud_turno.html', {
        'form': form,
        'enviado': enviado
    })
