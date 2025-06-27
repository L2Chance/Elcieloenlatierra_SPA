from django.urls import path
from . import views

urlpatterns = [
    path('registro-profesional/', views.registrar_profesional, name='registro_profesional'),
    path('solicitudes/', views.listar_solicitudes_profesionales, name='listar_solicitudes_profesionales'),
    path('aprobar-profesional/<int:profesional_id>/', views.aprobar_profesional, name='aprobar_profesional'),
    path('rechazar-profesional/<int:profesional_id>/', views.rechazar_profesional, name='rechazar_profesional'),
    path('perfil/profesional', views.mostrar_perfil_profesional, name="perfil_profesional"),
    path('profesional/exportar-turnos/', views.exportar_turnos_pdf, name='exportar_turnos_pdf'),

]