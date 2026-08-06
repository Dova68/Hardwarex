from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("login/", views.login, name="login"),
    path("historial/", views.historial, name="historial"),
    path("perfil/", views.perfil, name="perfil"),
    path("tecnico/", views.tecnico, name="tecnico"),
]