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