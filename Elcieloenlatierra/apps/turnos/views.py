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
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from django.core.mail import EmailMessage


from .forms import TurnoForm

from django.contrib.auth.decorators import login_required
from apps.reservas.models import Reserva  # ajusta la ruta si es diferente

def generar_comprobante_pdf(reserva):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin = 2 * cm
    box_width = width - 2 * margin
    box_height = height - 2 * margin

    # Recuadro
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

    # Datos reserva
    p.setFont("Helvetica", 12)
    y = height - 5 * cm

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


    # Footer
    p.setFont("Helvetica-Oblique", 10)
    p.setFillColor(colors.grey)
    p.drawCentredString(width / 2, margin + 1 * cm, "Gracias por confiar en Sentirse Bien SPA")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

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

    enviado = False

    if request.method == 'POST':
        formset = TurnoFormSet(request.POST, queryset=Turno.objects.none())
        for form in formset.forms:
            servicio_id = form.data.get(f'{form.prefix}-servicio')
            if servicio_id:
                form.__init__(form.data, servicio_id=servicio_id)

        if formset.is_valid():
            reservas_guardadas = []
            for form in formset:
                reserva = form.save(commit=False)
                reserva.usuario = request.user
                reserva.save()
                reservas_guardadas.append(reserva)

            # Generar y enviar correo con PDF por cada reserva
            for reserva in reservas_guardadas:
                pdf_buffer = generar_comprobante_pdf(reserva)
                email = EmailMessage(
                    subject='Comprobante de Reserva - Sentirse Bien SPA',
                    body='Adjuntamos el comprobante de su reserva. Gracias por elegirnos.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[reserva.usuario.email],
                )
                email.attach(f'comprobante_reserva_{reserva.id}.pdf', pdf_buffer.read(), 'application/pdf')
                email.send()

            enviado = True
            formset = TurnoFormSet(queryset=Turno.objects.none())
        else:
            enviado = False
    else:
        formset = TurnoFormSet(queryset=Turno.objects.none())

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