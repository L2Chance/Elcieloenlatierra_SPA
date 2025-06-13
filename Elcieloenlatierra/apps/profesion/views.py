from django.shortcuts import render, redirect
from .forms import ProfesionForm

def crear_profesion(request):
    if request.method == 'POST':
        form = ProfesionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('panel_control') 
    else:
        form = ProfesionForm()
    
    return render(request, 'profesional/crear-profesion.html', {'form': form})
