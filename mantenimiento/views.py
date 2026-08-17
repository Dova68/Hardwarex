from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import ( Usuario,Equipo,TipoEquipo,Ubicacion,SolicitudReparacion,Asignacion,Rol)

def inicio(request):

    if "id_usuario" not in request.session:
        return redirect("login")

    usuario = Usuario.objects.get(
        id_usuario=request.session["id_usuario"]
    )
    # REGISTRAR SOLICITUD
    if request.method == "POST":

        id_equipo = request.POST.get("id_equipo")
        tipo_falla = request.POST.get("tipo_falla")
        prioridad = request.POST.get("prioridad")
        descripcion = request.POST.get("descripcion")

        equipo = Equipo.objects.get(
            id_equipo=id_equipo
        )

        SolicitudReparacion.objects.create(
            id_usuario_fk=usuario,
            id_equipo_fk=equipo,
            descripcion=descripcion,
            prioridad_usuario=prioridad,
            fecha_solicitud=timezone.now(),
            estado="en_proceso"
        )

        messages.success(
            request,
            "Solicitud enviada correctamente."
        )

        return redirect("inicio")
    # MOSTRAR EQUIPOS
    equipos = Equipo.objects.select_related(
        "id_tipo_equipo_fk",
        "id_ubicacion_fk"
    ).all()

    return render(
        request,
        "index.html",
        {
            "usuario": usuario,
            "equipos": equipos
        }
    )


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
                request.session["id_rol_fk"] = usuario.id_rol_fk_id

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

        # Buscar el rol 2 en la tabla rol
        rol = Rol.objects.get(id_rol=2)

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
            id_rol_fk=rol
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

    if request.method == "POST":

        usuario.nombres = request.POST.get("nombres")
        usuario.apellidos = request.POST.get("apellidos")
        usuario.numero_tel = request.POST.get("numero_tel")
        usuario.nombre_usuario = request.POST.get("nombre_usuario")
        usuario.email = request.POST.get("email")
        usuario.fecha_nacimiento = request.POST.get("fecha_nacimiento")

        usuario.save()

        # Actualizar también los datos guardados en la sesión
        request.session["nombre_usuario"] = usuario.nombre_usuario
        request.session["nombres"] = usuario.nombres
        request.session["apellidos"] = usuario.apellidos
        request.session["email"] = usuario.email
        request.session["numero_tel"] = usuario.numero_tel
        request.session["fecha_nacimiento"] = usuario.fecha_nacimiento
        messages.success(
            request,
            "Datos actualizados correctamente."
        )

        return redirect("perfil")

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

    solicitudes = SolicitudReparacion.objects.select_related(
        "id_usuario_fk",
        "id_equipo_fk",
        "id_equipo_fk__id_tipo_equipo_fk"
    ).order_by("-fecha_solicitud")

    total_reportes = solicitudes.count()

    contexto = {
        "solicitudes": solicitudes,
        "total_reportes": total_reportes,
    }

    return render(
        request,
        "admin_home.html",
        contexto
    )

def reportes_recientes(request):

    # ASIGNAR SOLICITUD A TÉCNICO
    if request.method == "POST":

        id_solicitud = request.POST.get("id_solicitud")
        id_tecnico = request.POST.get("id_tecnico")

        solicitud = SolicitudReparacion.objects.get(
            id_solicitud=id_solicitud
        )

        tecnico = Usuario.objects.get(
            id_usuario=id_tecnico
        )

        # Crear la asignación
        Asignacion.objects.create(
            id_solicitud_fk=solicitud,
            id_tecnico_fk=tecnico,
            prioridad_asignada=solicitud.prioridad_usuario,
            fecha_asignacion=timezone.now(),
            estado_asignacion="asignado"
        )

        # Cambiar estado de la solicitud
        solicitud.estado = "en_proceso"
        solicitud.save()

        messages.success(
            request,
            "Solicitud asignada correctamente al técnico."
        )

        return redirect("reportes_recientes")


    # MOSTRAR SOLICITUDES PENDIENTES
    reportes = SolicitudReparacion.objects.select_related(
        "id_usuario_fk",
        "id_equipo_fk",
        "id_equipo_fk__id_tipo_equipo_fk",
        "id_equipo_fk__id_ubicacion_fk"
    ).filter(
        estado="pendiente"
    ).order_by("-fecha_solicitud")


    # TÉCNICOS
    tecnicos = Usuario.objects.filter(
        id_rol_fk_id=3
    )


    return render(
        request,
        "reportes_recientes.html",
        {
            "reportes": reportes,
            "tecnicos": tecnicos
        }
    )


def tecnicos_admin(request):
    return render(request, "tecnicos.html")


def historial_admin(request):
    return render(request, "historial_admin.html")


def equipos_admin(request):
    # POS

    if request.method == 'POST':

        accion = request.POST.get('accion')

        # AGREGAR

        if accion == 'agregar':

            codigo = request.POST.get('codigo')
            tipo_equipo = request.POST.get('tipo_equipo')
            fecha_compra = request.POST.get('fecha_compra')
            ubicacion = request.POST.get('ubicacion')
            estado_general = request.POST.get('estado_general')

            Equipo.objects.create(
                codigo=codigo,
                id_tipo_equipo_fk_id=tipo_equipo,
                fecha_compra=fecha_compra if fecha_compra else None,
                id_ubicacion_fk_id=ubicacion if ubicacion else None,
                estado_general=estado_general
            )

            return redirect('equipos_admin')


        # ACTUALIZAR

        elif accion == 'actualizar':

            id_equipo = request.POST.get('id_equipo')

            equipo = Equipo.objects.get(
                id_equipo=id_equipo
            )

            equipo.codigo = request.POST.get('codigo')

            equipo.id_tipo_equipo_fk_id = request.POST.get(
                'tipo_equipo'
            )

            fecha_compra = request.POST.get('fecha_compra')

            equipo.fecha_compra = (
                fecha_compra if fecha_compra else None
            )

            ubicacion = request.POST.get('ubicacion')

            equipo.id_ubicacion_fk_id = (
                ubicacion if ubicacion else None
            )

            equipo.estado_general = request.POST.get(
                'estado_general'
            )

            equipo.save()

            return redirect('equipos_admin')


        # ELIMINAR

        elif accion == 'eliminar':

            id_equipo = request.POST.get('id_equipo')

            equipo = Equipo.objects.get(
                id_equipo=id_equipo
            )

            equipo.delete()

            return redirect('equipos_admin')

    # MOSTRAR EQUIPO

    equipos = Equipo.objects.select_related(
        'id_tipo_equipo_fk',
        'id_ubicacion_fk'
    ).all()

    tipos_equipo = TipoEquipo.objects.all()

    ubicaciones = Ubicacion.objects.all()

    # DATOS PARA JAVASCRIP

    equipos_json = []

    for equipo in equipos:

        equipos_json.append({
            'id': equipo.id_equipo,
            'codigo': equipo.codigo,
            'tipo': equipo.id_tipo_equipo_fk.id_tipo_equipo,
            'fecha': equipo.fecha_compra.strftime('%Y-%m-%d')
                if equipo.fecha_compra else '',
            'ubicacion': equipo.id_ubicacion_fk.id_ubicacion
                if equipo.id_ubicacion_fk else '',
            'estado': equipo.estado_general,
        })


    contexto = {
        'equipos': equipos,
        'tipos_equipo': tipos_equipo,
        'ubicaciones': ubicaciones,
        'equipos_json': equipos_json,
    }


    return render(
        request,
        'equipos_admin.html',
        contexto
    )



def piezas(request):
    return render(request, "piezas.html")


def asignaciones(request):
    return render(request, "asignaciones.html")


def logout(request):

    request.session.flush()

    return redirect("login")