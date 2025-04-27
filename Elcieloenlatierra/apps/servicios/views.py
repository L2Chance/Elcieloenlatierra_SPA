from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import ServicioForm
from .models import Servicio
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

#FUNCIÓN PARA LISTAR SERVICIO

def listar_servicios(request):
    servicios = Servicio.objects.all()
    form_vacio = ServicioForm() 
    context = {'servicios': servicios, 'form': form_vacio}
    return render(request, 'servicios/servicios.html', context)


#FUNCIÓN PARA CREAR SERVICIO

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


#FUNCIÓN PARA MODIFICAR SERVICIO

def modificar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    exito = False

    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES, instance=servicio)
        if form.is_valid():
            form.save()
            exito = True
    else:
        form = ServicioForm(instance=servicio)

    return render(request, 'servicios/formularios/modificar_servicio.html', {'form': form, 'exito': exito, 'servicio': servicio})

#FUNCIÓN PARA ELIMINAR SERVICIO

def eliminar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)

    if request.method == 'POST':
        servicio.delete()
        return redirect('listar_servicios') 
    else:
        return render(request, 'servicios/formularios/eliminar_servicio.html', {'servicio': servicio})