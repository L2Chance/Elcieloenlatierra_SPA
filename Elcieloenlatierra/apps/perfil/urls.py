from . import views
from django.urls import path


urlpatterns = [
    path('perfil/', views.editar_perfil, name='editar_perfil'),
]