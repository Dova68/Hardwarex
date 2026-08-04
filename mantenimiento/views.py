from django.shortcuts import render

def inicio(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def historial(request):
    return render(request, "historial.html")

def tecnico(request):
    return render(request, "tecnico.html")