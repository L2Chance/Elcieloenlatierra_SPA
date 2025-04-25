from django.shortcuts import render, redirect
from .forms import ServicioForm
from .models import Servicio
from django.contrib.auth.decorators import login_required

@login_required
def crear_servicio(request):
    exito = False 
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            exito = True  
            return redirect('/home')  
    else:
        form = ServicioForm()
    
    return render(request, 'servicios/formularios/nuevo_servicio.html', {'form': form, 'exito': exito})

def listar_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicios/servicios.html', {'servicios': servicios})