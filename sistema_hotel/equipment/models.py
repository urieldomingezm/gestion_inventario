from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'categorias'

    def __str__(self):
        return self.nombre

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'ubicaciones'

    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    ESTADO_CHOICES = [
        ('Operativo', 'Operativo'),
        ('En mantenimiento', 'En mantenimiento'),
        ('Fuera de servicio', 'Fuera de servicio'),
        ('Descontinuado', 'Descontinuado')
    ]

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(null=True, blank=True)
    numero_serie = models.CharField(max_length=100, unique=True)
    marca = models.CharField(max_length=100, null=True, blank=True)
    modelo = models.CharField(max_length=100, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, db_column='categoria_id')
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True, db_column='ubicacion_id')
    fecha_adquisicion = models.DateField(null=True, blank=True)
    fecha_garantia = models.DateField(null=True, blank=True)
    fecha_expericion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Operativo')

    class Meta:
        db_table = 'equipos'

    def __str__(self):
        return f"{self.nombre} - {self.numero_serie}"

class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('Asignación', 'Asignación'),
        ('Cambio de ubicación', 'Cambio de ubicación'),
        ('Mantenimiento', 'Mantenimiento'),
        ('Baja', 'Baja')
    ]

    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='equipo_id')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField(null=True, blank=True)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    usuario_responsable = models.CharField(max_length=150, null=True, blank=True)
    nueva_ubicacion = models.ForeignKey(Ubicacion, on_delete=models.SET_NULL, null=True, db_column='nueva_ubicacion_id')

    class Meta:
        db_table = 'movimientos'

    def __str__(self):
        return f"{self.tipo} - {self.equipo.nombre} ({self.fecha_movimiento})"
