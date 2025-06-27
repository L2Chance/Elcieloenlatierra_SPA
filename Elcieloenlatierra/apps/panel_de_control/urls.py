# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('panel/', views.mostrar_panel_de_control, name='panel_control'),

    # Servicios
    path('panel/servicio/nuevo/', views.crear_servicio, name='crear_servicio'),
    path('panel/servicio/<int:pk>/editar/', views.editar_servicio, name='editar_servicio'),
    path('panel/servicio/<int:pk>/eliminar/', views.eliminar_servicio, name='eliminar_servicio'),

    # Profesiones
    path('panel/profesion/nueva/', views.crear_profesion, name='crear_profesion'),
    path('panel/profesion/<int:pk>/editar/', views.editar_profesion, name='editar_profesion'),
    path('panel/profesion/<int:pk>/eliminar/', views.eliminar_profesion, name='eliminar_profesion'),

    # Profesionales
    path('panel/aprobar-profesional/<int:profesional_id>/', views.aprobar_profesional, name='aprobar_profesional'),
    path('panel/rechazar-profesional/<int:profesional_id>/', views.rechazar_profesional, name='rechazar_profesional'),
    path('eliminar-profesional/<int:profesional_id>/', views.eliminar_profesional, name='eliminar_profesional'),

    #Roles
    path('asignar-rol/', views.asignar_rol, name='asignar_rol'),

    path('eliminar-usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),



]
