from django.shortcuts import render
from .forms import ContactoForm

def contacto(request):
    enviado = False
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            print("📩 Nuevo mensaje de contacto recibido:")
            print(f"Nombre: {datos['nombre']} {datos['apellido']}")
            print(f"Teléfono: {datos['telefono']}")
            print(f"Correo: {datos['correo']}")
            print(f"Motivo: {datos['motivo']}")
            print("Comentarios:")
            print(datos['comentarios'])
            print("✅ Fin del mensaje.\n")

            enviado = True
            form = ContactoForm()
    else:
        form = ContactoForm()
    
    return render(request, 'contacto/formularios/formulario_contacto.html', {
        'form': form,
        'enviado': enviado
    })