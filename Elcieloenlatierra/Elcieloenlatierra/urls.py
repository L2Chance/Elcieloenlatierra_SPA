""" 
Este es el archivo urls.py. Acá, como es notorio, controlamos las urls y el enrutamiento de nuestro 
sitio.

path('home', views.mostrar_base) es la estructura básica para definir una url. 

'home': es lo que vendrá inmediatamente luego del dominio de nuestro sitio 'Misitio/home'

'views.mostrar_home': mostrar_home es la función definida en mi archivo views.py. Ahí indique
que esa función debe mostrar el archivo home.html.

"""

from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mostrar_home),
    path('home', views.mostrar_home),
    path('login', views.mostrar_login),
    path('turno', views.mostrar_turno),

]
