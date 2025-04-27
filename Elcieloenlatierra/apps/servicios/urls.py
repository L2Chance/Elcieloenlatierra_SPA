from django.urls import path
from . import views

urlpatterns = [
    path('nuevo/', views.crear_servicio, name='crear_servicio'),
    path('listado/', views.listar_servicios, name='listar_servicios'),
    path('modificar/<int:pk>/', views.modificar_servicio, name='modificar_servicio'),
    path('eliminar/<int:pk>/', views.eliminar_servicio, name='modificar_servicio')
]