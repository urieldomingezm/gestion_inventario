from django.contrib import admin
from .models import Categoria, Ubicacion, Equipo, Movimiento

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero_serie', 'marca', 'modelo', 'categoria', 'ubicacion', 'estado')
    list_filter = ('estado', 'categoria', 'ubicacion')
    search_fields = ('nombre', 'numero_serie', 'marca', 'modelo')
    date_hierarchy = 'fecha_adquisicion'

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'tipo', 'fecha_movimiento', 'usuario_responsable')
    list_filter = ('tipo', 'fecha_movimiento')
    search_fields = ('equipo__nombre', 'usuario_responsable')
    date_hierarchy = 'fecha_movimiento'
