# apps/turnos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('turno/', views.solicitud_turno, name='solicitud_turno'),
    path('cancelar-turno/<int:turno_id>/', views.cancelar_turno, name='cancelar_turno'),
]