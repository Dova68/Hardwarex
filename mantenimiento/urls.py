from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("login/", views.login, name="login"),
    path("historial/", views.historial, name="historial"),
    path("register/", views.register, name="register"),
    path("perfil/", views.perfil, name="perfil"),
    path("tecnico/", views.tecnico, name="tecnico"),
    path("equipos/", views.equipos, name="equipos"),
    path("solicitudes/", views.solicitudes, name="solicitudes"),
    path("mantenimientos/", views.mantenimientos, name="mantenimientos"),
    path("reportes/", views.reportes, name="reportes"),
    path("perfil-tecnico/", views.perfil_tecnico, name="perfil_tecnico"),
    path("admin-home/", views.admin_home, name="admin_home"),
    path("reportes-recientes/", views.reportes_recientes, name="reportes_recientes"),
    path("tecnicos-admin/", views.tecnicos_admin, name="tecnicos_admin"),
    path("historial-admin/", views.historial_admin, name="historial_admin"),
    path("equipos-admin/", views.equipos_admin, name="equipos_admin"),
    path("piezas/", views.piezas, name="piezas"),
    path("asignaciones/", views.asignaciones, name="asignaciones"),
    path("logout/", views.logout, name="logout"),
]