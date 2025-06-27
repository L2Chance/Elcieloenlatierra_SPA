# roles/urls.py
from django.urls import path
from .views import crear_rol

urlpatterns = [
    path('crear/', crear_rol, name='crear_rol'),
    path('crear-rol/', crear_rol, name='crear_rol'),
]