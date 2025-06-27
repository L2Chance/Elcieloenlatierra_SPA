from django.shortcuts import render
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from .forms import CrearRolForm

def crear_rol(request):
    if request.method == 'POST':
        form = CrearRolForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            permisos = form.cleaned_data['permisos']
            
            grupo, creado = Group.objects.get_or_create(name=nombre)
            grupo.permissions.set(permisos)
            grupo.save()
            return redirect('panel_control')  # O a donde quieras redirigir
    else:
        form = CrearRolForm()

    return render(request, 'roles/crear-roles.html', {'form': form})