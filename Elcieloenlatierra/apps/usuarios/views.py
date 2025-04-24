# cuentas/views.py
from django.shortcuts import render, redirect
from .forms import RegistroForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

"""Este método se encarga de no permitir el acceso al formulario de
registro a usuarios que ya estén autenticados en la pagina"""

def usuario_no_autenticado(view_func):
    return user_passes_test(lambda u: not u.is_authenticated, login_url='/home')(view_func)

@usuario_no_autenticado
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})

from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

#Esta clase se encarga de que si el usuario ya está autenticado, no pueda entrar al formulario de login

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)