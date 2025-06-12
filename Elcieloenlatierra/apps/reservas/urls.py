from django.urls import path
from . import views

urlpatterns = [
    path('reservar/', views.reservar_turno, name='reservar_turno'),
    path('reservas/eliminar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
]
