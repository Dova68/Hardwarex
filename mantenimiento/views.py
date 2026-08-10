from django.shortcuts import render


def inicio(request):
    return render(request, "index.html")


def login(request):
    return render(request, "login.html")


def historial(request):
    return render(request, "historial.html")


def perfil(request):
    return render(request, "perfil.html")


def tecnico(request):
    return render(request, "tecnico.html")


def equipos(request):
    return render(request, "equipos.html")


def solicitudes(request):
    return render(request, "solicitudes.html")


def mantenimientos(request):
    return render(request, "mantenimientos.html")


def reportes(request):
    return render(request, "reportes.html")


def perfil_tecnico(request):
    return render(request, "perfil_tecnico.html")