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
from django.core.mail import EmailMessage
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import modelformset_factory
from .models import Reserva, Servicio
from .forms import ReservaForm
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def generar_comprobante_pdf(reserva):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Margen
    margin = 2 * cm
    box_width = width - 2 * margin
    box_height = height - 2 * margin

    # Dibujar recuadro
    p.setStrokeColor(colors.grey)
    p.setLineWidth(1)
    p.rect(margin, margin, box_width, box_height)

    # Título
    p.setFont("Helvetica-Bold", 20)
    p.drawCentredString(width / 2, height - 3 * cm, "Comprobante de Reserva")

    # Línea divisoria
    p.setStrokeColor(colors.black)
    p.setLineWidth(0.5)
    p.line(margin + 1 * cm, height - 3.5 * cm, width - margin - 1 * cm, height - 3.5 * cm)

    # Datos
    p.setFont("Helvetica", 12)
    y = height - 5 * cm  # Punto de inicio

    datos = [
        ("Nombre", f"{reserva.usuario.perfil.primer_nombre} {reserva.usuario.perfil.apellido}"),
        ("Email", reserva.usuario.email),
        ("Servicio", reserva.servicio.nombre),
        ("Precio", f"${reserva.servicio.precio:.2f}"),
        ("Fecha de reserva", reserva.fecha.strftime('%d/%m/%Y')),
    ]

    for label, value in datos:
        p.drawString(margin + 1.5 * cm, y, f"{label}:")
        p.setFont("Helvetica-Bold", 12)
        p.drawString(margin + 5.5 * cm, y, value)
        p.setFont("Helvetica", 12)
        y -= 1.2 * cm

    # Mensaje adicional antes del footer
    p.setFont("Helvetica-Oblique", 11)
    p.setFillColor(colors.darkgray)
    mensaje = "Su reserva será gestionada por un administrador, quien asignará un horario disponible acorde al turno solicitado. Recibirá una confirmación por correo cuando su turno esté confirmado."
    p.drawCentredString(width / 2, margin + 3 * cm, mensaje)

    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.setFillColor(colors.grey)
    p.drawCentredString(width / 2, margin + 1 * cm, "Gracias por confiar en Sentirse Bien SPA")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


def reservar_turno(request):
    servicios = Servicio.objects.all()
    servicios_turnos = {servicio.id: servicio.turnos for servicio in servicios}

    ReservaFormSet = modelformset_factory(
        Reserva,          
        form=ReservaForm,
        extra=1,
        can_delete=True,
    )

    if request.method == 'POST':
        formset = ReservaFormSet(request.POST, queryset=Reserva.objects.none())  

        if formset.is_valid():
            for form in formset:
                reserva = form.save(commit=False)
                reserva.usuario = request.user
                reserva.save()


                pdf_buffer = generar_comprobante_pdf(reserva)


                subject = "Comprobante de tu reserva"
                message = "Gracias por reservar en Sentirse Bien Spa. Adjuntamos el comprobante en PDF."
                email = EmailMessage(
                    subject,
                    message,
                    to=[reserva.usuario.email],
                )
                email.attach("comprobante.pdf", pdf_buffer.read(), "application/pdf")
                email.send()
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
    reserva = get_object_or_404(Reserva, id=reserva_id)  # ← quitamos usuario=request.user

    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "Reserva cancelada correctamente.")
        return redirect('/turno')

    messages.error(request, "Método no permitido.")
    return redirect('vista_donde_listas_reservas')