from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("login/", views.login, name="login"),
    path("historial/", views.historial, name="historial"),
    path("tecnico/", views.tecnico, name="tecnico"),
]