from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario


def inicio(request):
    return render(request, "index.html")


def login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        clave = request.POST.get("clave")

        try:
            usuario = Usuario.objects.get(email=email)

            if usuario.clave == clave:

                # Guardar datos del usuario en la sesión
                request.session["id_usuario"] = usuario.id_usuario
                request.session["nombre_usuario"] = usuario.nombre_usuario
                request.session["nombres"] = usuario.nombres
                request.session["apellidos"] = usuario.apellidos
                request.session["email"] = usuario.email
                request.session["id_rol_fk"] = usuario.id_rol_fk

                # Redirigir al perfil
                return redirect("perfil")

            else:
                messages.error(
                    request,
                    "La contraseña es incorrecta."
                )

        except Usuario.DoesNotExist:

            messages.error(
                request,
                "El usuario no existe."
            )

    return render(request, "login.html")


def register(request):

    if request.method == "POST":

        nombres = request.POST.get("nombres")
        apellidos = request.POST.get("apellidos")
        numero_tel = request.POST.get("numero_tel")
        nombre_usuario = request.POST.get("nombre_usuario")
        email = request.POST.get("email")
        fecha_nacimiento = request.POST.get("fecha_nacimiento")
        clave = request.POST.get("clave")

        # Todos los usuarios registrados tendrán el rol 2
        id_rol_fk = 2

        # Comprobar nombre de usuario
        if Usuario.objects.filter(
            nombre_usuario=nombre_usuario
        ).exists():

            messages.error(
                request,
                "Ese nombre de usuario ya existe."
            )

            return redirect("register")

        # Comprobar correo
        if Usuario.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Ese correo ya está registrado."
            )

            return redirect("register")

        # Crear usuario
        Usuario.objects.create(
            clave=clave,
            nombres=nombres,
            apellidos=apellidos,
            numero_tel=numero_tel,
            nombre_usuario=nombre_usuario,
            email=email,
            fecha_nacimiento=fecha_nacimiento,
            id_rol_fk=id_rol_fk
        )

        messages.success(
            request,
            "Usuario registrado correctamente."
        )

        return redirect("login")

    return render(request, "login.html")


def historial(request):
    return render(request, "historial.html")


def perfil(request):

    if "id_usuario" not in request.session:
        return redirect("login")

    usuario = Usuario.objects.get(
        id_usuario=request.session["id_usuario"]
    )

    return render(
        request,
        "perfil.html",
        {
            "usuario": usuario
        }
    )


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


def admin_home(request):
    return render(request, "admin_home.html")


def reportes_recientes(request):
    return render(request, "reportes_recientes.html")


def tecnicos_admin(request):
    return render(request, "tecnicos.html")


def historial_admin(request):
    return render(request, "historial_admin.html")


def equipos_admin(request):
    return render(request, "equipos_admin.html")


def piezas(request):
    return render(request, "piezas.html")


def asignaciones(request):
    return render(request, "asignaciones.html")
