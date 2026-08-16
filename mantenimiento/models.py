from django.db import models



class Rol(models.Model):

    id_rol = models.AutoField(primary_key=True)

    nombre_rol = models.CharField(
        max_length=50,
        unique=True
    )

    descripcion_rol = models.TextField(
        null=True,
        blank=True
    )

    estado_rol = models.CharField(
        max_length=20
    )

    class Meta:
        managed = False
        db_table = "rol"

    def __str__(self):
        return self.nombre_rol


class Usuario(models.Model):

    id_usuario = models.AutoField(primary_key=True)

    clave = models.CharField(
        max_length=255
    )

    nombres = models.CharField(
        max_length=100
    )

    apellidos = models.CharField(
        max_length=100
    )

    numero_tel = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    nombre_usuario = models.CharField(
        max_length=50,
        unique=True
    )

    email = models.CharField(
        max_length=100,
        unique=True
    )

    fecha_nacimiento = models.DateField(
        null=True,
        blank=True
    )

    id_rol_fk = models.ForeignKey(
        Rol,
        on_delete=models.DO_NOTHING,
        db_column="id_rol_fk"
    )

    class Meta:
        managed = False
        db_table = "usuario"

    def __str__(self):
        return self.nombre_usuario



class TipoEquipo(models.Model):

    id_tipo_equipo = models.AutoField(primary_key=True)

    nombre_tipo = models.CharField(
        max_length=30,
        unique=True
    )

    class Meta:
        managed = False
        db_table = "tipo_equipo"

    def __str__(self):
        return self.nombre_tipo


class Ubicacion(models.Model):

    id_ubicacion = models.AutoField(primary_key=True)

    sede = models.CharField(
        max_length=100
    )

    salon = models.CharField(
        max_length=20
    )

    class Meta:
        managed = False
        db_table = "ubicacion"
        unique_together = ("sede", "salon")

    def __str__(self):
        return f"{self.sede} - {self.salon}"


class Equipo(models.Model):

    id_equipo = models.AutoField(primary_key=True)

    codigo = models.CharField(
        max_length=100,
        unique=True
    )

    id_tipo_equipo_fk = models.ForeignKey(
        TipoEquipo,
        on_delete=models.DO_NOTHING,
        db_column="id_tipo_equipo_fk"
    )

    fecha_compra = models.DateField(
        null=True,
        blank=True
    )

    id_ubicacion_fk = models.ForeignKey(
        Ubicacion,
        on_delete=models.DO_NOTHING,
        db_column="id_ubicacion_fk",
        null=True,
        blank=True
    )

    estado_general = models.CharField(
        max_length=20
    )

    class Meta:
        managed = False
        db_table = "equipo"

    def __str__(self):
        return self.codigo




class TipoPieza(models.Model):

    id_tipo_pieza = models.AutoField(primary_key=True)

    nombre = models.CharField(
        max_length=50,
        unique=True
    )

    descripcion = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = "tipo_pieza"

    def __str__(self):
        return self.nombre


class Marca(models.Model):

    id_marca = models.AutoField(primary_key=True)

    nombre_marca = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        managed = False
        db_table = "marca"

    def __str__(self):
        return self.nombre_marca


class ModeloPieza(models.Model):

    id_modelo = models.AutoField(primary_key=True)

    id_marca_fk = models.ForeignKey(
        Marca,
        on_delete=models.DO_NOTHING,
        db_column="id_marca_fk"
    )

    id_tipo_pieza_fk = models.ForeignKey(
        TipoPieza,
        on_delete=models.DO_NOTHING,
        db_column="id_tipo_pieza_fk"
    )

    nombre_modelo = models.CharField(
        max_length=100
    )

    especificaciones = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = "modelo_pieza"
        unique_together = (
            "id_marca_fk",
            "nombre_modelo"
        )

    def __str__(self):
        return self.nombre_modelo


class Pieza(models.Model):

    id_pieza = models.AutoField(primary_key=True)

    id_modelo_fk = models.ForeignKey(
        ModeloPieza,
        on_delete=models.DO_NOTHING,
        db_column="id_modelo_fk"
    )

    numero_serie = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )

    estado = models.CharField(
        max_length=20
    )

    fecha_registro = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "pieza"

    def __str__(self):
        return self.numero_serie or f"Pieza {self.id_pieza}"


class SolicitudReparacion(models.Model):

    id_solicitud = models.AutoField(primary_key=True)

    id_usuario_fk = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING,
        db_column="id_usuario_fk"
    )

    id_equipo_fk = models.ForeignKey(
        Equipo,
        on_delete=models.DO_NOTHING,
        db_column="id_equipo_fk"
    )

    descripcion = models.TextField()

    prioridad_usuario = models.CharField(
        max_length=10
    )

    fecha_solicitud = models.DateTimeField()

    estado = models.CharField(
        max_length=20
    )

    class Meta:
        managed = False
        db_table = "solicitud_reparacion"

    def __str__(self):
        return f"Solicitud {self.id_solicitud}"


class Falla(models.Model):

    id_falla = models.AutoField(primary_key=True)

    id_solicitud_fk = models.ForeignKey(
        SolicitudReparacion,
        on_delete=models.DO_NOTHING,
        db_column="id_solicitud_fk"
    )

    tipo_falla = models.CharField(
        max_length=20
    )

    descripcion_tecnica = models.TextField(
        null=True,
        blank=True
    )

    fecha_deteccion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "falla"

    def __str__(self):
        return f"Falla {self.id_falla}"



class Asignacion(models.Model):

    id_asignacion = models.AutoField(primary_key=True)

    id_solicitud_fk = models.ForeignKey(
        SolicitudReparacion,
        on_delete=models.DO_NOTHING,
        db_column="id_solicitud_fk"
    )

    id_tecnico_fk = models.ForeignKey(
        Usuario,
        on_delete=models.DO_NOTHING,
        db_column="id_tecnico_fk"
    )

    prioridad_asignada = models.CharField(
        max_length=10
    )

    fecha_asignacion = models.DateTimeField()

    estado_asignacion = models.CharField(
        max_length=20
    )

    class Meta:
        managed = False
        db_table = "asignacion"

    def __str__(self):
        return f"Asignación {self.id_asignacion}"


class Mantenimiento(models.Model):

    id_mantenimiento = models.AutoField(primary_key=True)

    id_asignacion_fk = models.ForeignKey(
        Asignacion,
        on_delete=models.DO_NOTHING,
        db_column="id_asignacion_fk"
    )

    tipo = models.CharField(
        max_length=20
    )

    fecha_inicio = models.DateTimeField(
        null=True,
        blank=True
    )

    fecha_fin = models.DateTimeField(
        null=True,
        blank=True
    )

    descripcion = models.TextField(
        null=True,
        blank=True
    )

    archivo_ruta = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = "mantenimiento"

    def __str__(self):
        return f"Mantenimiento {self.id_mantenimiento}"


class ProcesoReparacion(models.Model):

    id_proceso = models.AutoField(primary_key=True)

    id_mantenimiento_fk = models.ForeignKey(
        Mantenimiento,
        on_delete=models.DO_NOTHING,
        db_column="id_mantenimiento_fk"
    )

    nombre = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    observacion = models.TextField(
        null=True,
        blank=True
    )

    estado = models.CharField(
        max_length=20
    )

    fecha_inicio = models.DateTimeField(
        null=True,
        blank=True
    )

    fecha_esperada = models.DateTimeField(
        null=True,
        blank=True
    )

    fecha_fin = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = "proceso_reparacion"

    def __str__(self):
        return self.nombre or f"Proceso {self.id_proceso}"



class HistorialPieza(models.Model):

    id_historial = models.AutoField(primary_key=True)

    id_pieza_fk = models.ForeignKey(
        Pieza,
        on_delete=models.DO_NOTHING,
        db_column="id_pieza_fk"
    )

    id_equipo_origen_fk = models.ForeignKey(
        Equipo,
        on_delete=models.DO_NOTHING,
        db_column="id_equipo_origen_fk",
        null=True,
        blank=True,
        related_name="historial_origen"
    )

    id_equipo_destino_fk = models.ForeignKey(
        Equipo,
        on_delete=models.DO_NOTHING,
        db_column="id_equipo_destino_fk",
        null=True,
        blank=True,
        related_name="historial_destino"
    )

    fecha_cambio = models.DateTimeField()

    motivo = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )

    id_mantenimiento_fk = models.ForeignKey(
        Mantenimiento,
        on_delete=models.DO_NOTHING,
        db_column="id_mantenimiento_fk",
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = "historial_pieza"

    def __str__(self):
        return f"Historial {self.id_historial}"



class Recordatorio(models.Model):

    id_recordatorio = models.AutoField(primary_key=True)

    descripcion = models.TextField(
        null=True,
        blank=True
    )

    fecha = models.DateField()

    hora = models.TimeField(
        null=True,
        blank=True
    )

    estado = models.CharField(
        max_length=20
    )

    id_mantenimiento_fk = models.ForeignKey(
        Mantenimiento,
        on_delete=models.DO_NOTHING,
        db_column="id_mantenimiento_fk",
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = "recordatorio"

    def __str__(self):
        return f"Recordatorio {self.id_recordatorio}"


class Advertencia(models.Model):

    id_advertencia = models.AutoField(primary_key=True)

    mensaje = models.TextField()

    fecha_hora = models.DateTimeField()

    id_solicitud_fk = models.ForeignKey(
        SolicitudReparacion,
        on_delete=models.DO_NOTHING,
        db_column="id_solicitud_fk",
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = "advertencia"

    def __str__(self):
        return f"Advertencia {self.id_advertencia}"



class Proveedor(models.Model):

    id_proveedor = models.AutoField(primary_key=True)

    contacto = models.CharField(
        max_length=30
    )

    nombre_proveedor = models.CharField(
        max_length=100
    )

    telefono = models.CharField(
        max_length=20
    )

    correo_electronico = models.CharField(
        max_length=100
    )

    class Meta:
        managed = False
        db_table = "proveedor"

    def __str__(self):
        return self.nombre_proveedor


class Garantia(models.Model):

    id_garantia = models.AutoField(primary_key=True)

    id_pieza_fk = models.ForeignKey(
        Pieza,
        on_delete=models.DO_NOTHING,
        db_column="id_pieza_fk"
    )

    id_proveedor_fk = models.ForeignKey(
        Proveedor,
        on_delete=models.DO_NOTHING,
        db_column="id_proveedor_fk"
    )

    fecha_inicio = models.DateField(
        null=True,
        blank=True
    )

    fecha_vencimiento = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        managed = False
        db_table = "garantia"

    def __str__(self):
        return f"Garantía {self.id_garantia}"