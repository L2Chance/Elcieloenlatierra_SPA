# apps/turnos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('turno/', views.solicitud_turno, name='solicitud_turno'),
    path('gracias/', views.dar_gracias, name='gracias')
]