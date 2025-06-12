from .models import Perfil 

def perfil_usuario(request):
    if request.user.is_authenticated:
        try:
            perfil = Perfil.objects.get(user=request.user)
            return {'perfil_usuario': perfil}
        except Perfil.DoesNotExist:
            return {'perfil_usuario': None}
    return {'perfil_usuario': None}