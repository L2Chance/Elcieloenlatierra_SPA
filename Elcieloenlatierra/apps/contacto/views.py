from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from .forms import ContactoForm

def contacto(request):
    datos = {}
    enviado = False

    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data

            asunto = "Nuevo mensaje de contacto"
            mensaje = (
                f"📩 Nuevo mensaje de contacto:\n\n"
                f"Nombre: {datos['nombre']} {datos['apellido']}\n"
                f"Teléfono: {datos['telefono']}\n"
                f"Correo: {datos['correo']}\n"
                f"Motivo: {datos['motivo']}\n"
                f"Comentarios:\n{datos['comentarios']}\n\n"
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
            form = ContactoForm() 
        else:
            print("❌ Errores en el formulario:", form.errors)
    else:
        form = ContactoForm()

    return render(request, 'contacto/formularios/formulario_contacto.html', {
        'form': form,
        'enviado': enviado,
        'datos': datos
    })