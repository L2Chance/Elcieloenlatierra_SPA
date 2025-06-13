from django.urls import path
from . import views

urlpatterns = [
    path('crear-profesion/', views.crear_profesion, name='crear_profesion'),
]