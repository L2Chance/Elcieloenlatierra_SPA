from . import views
from django.urls import path


urlpatterns = [
    path('perfil/registro', views.crear_primer_perfil, name='crear_primer_perfil'),
    path('perfil/editar', views.editar_perfil, name='editar_perfil'),
    path('perfil/registro', views.crear_perfil_usuario, name='crear_usuario'),
    path('perfil/detalle', views.detalle_perfil , name='detalle_perfil'),
]