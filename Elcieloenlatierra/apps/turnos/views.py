from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required



@login_required
def dar_gracias(request):
    return render(request, 'home.html')


def solicitud_turno(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        fecha = request.POST.get('fecha')
        servicio = request.POST.get('servicio')
        comentarios = request.POST.get('comentarios')

        asunto = f"Nuevo Turno Solicitado: {servicio}"
        mensaje = f"""
        📆 Se solicitó un turno.

        🧍 Nombre: {nombre}
        📧 Email: {email}
        📞 Teléfono: {telefono}
        🗓 Fecha: {fecha}
        💆 Servicio: {servicio}
        💬 Comentarios: {comentarios}
        """

        send_mail(
            asunto,
            mensaje,
            settings.EMAIL_HOST_USER,  # Remitente
            ['destinatario@ejemplo.com'],  # Cambia por el correo real de destino
            fail_silently=False,
        )

        return redirect('gracias')  # redirige a una vista de confirmación

    return render(request, 'solicitud_turno.html')