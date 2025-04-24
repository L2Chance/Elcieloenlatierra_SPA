"""Este es el archivo views. En este definiremos la lógica de lo que se va a mostrar en nuestra
pagina. Podemos simplemente mostrar un html en concreto, importar una api de peliculas, indicar
que en un html se van a mostrar 10 posters de peliculas y otros datos, controlar los cookies del
navegador para que el usuario no tenga que estár cargando de 0 nuestra pagina constantemente, etc...

En nuestro caso tenemos un proyecto simple, por lo que solo es necesario mostrar un html en concreto
de alguna pagina de nuestro sitio.

"""

from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy

def mostrar_home(request):
    return render(request, "home.html")

def mostrar_login(request):
    return render(request, "login.html")

def mostrar_servicios(request):
    return render(request, "servicios.html")


