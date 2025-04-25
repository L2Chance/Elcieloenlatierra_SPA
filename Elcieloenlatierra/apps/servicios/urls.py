from django.urls import path
from . import views

urlpatterns = [
    path('nuevo/', views.crear_servicio, name='crear_servicio'),
    path('listado/', views.listar_servicios, name='listar_servicios'),
]