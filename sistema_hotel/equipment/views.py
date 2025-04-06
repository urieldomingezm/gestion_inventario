from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Equipo, Ubicacion, Movimiento, Categoria  # Added Categoria import
from django.contrib.auth.decorators import login_required
from django.db.models import Count  # Add this import
import datetime  # Add this import

@login_required
def equipo_list(request):
    equipos = Equipo.objects.all()
    categorias = Categoria.objects.all()
    ubicaciones = Ubicacion.objects.all()
    
    # Calculate statistics
    equipos_operativos = equipos.filter(estado='Operativo').count()
    equipos_mantenimiento = equipos.filter(estado='En mantenimiento').count()
    equipos_fuera_servicio = equipos.filter(estado='Fuera de servicio').count()

    # Data for charts
    equipos_por_categoria = list(Equipo.objects.values('categoria__nombre')
                               .annotate(total=Count('id'))
                               .values_list('total', flat=True))
    categorias_labels = list(Equipo.objects.values_list('categoria__nombre', flat=True).distinct())

    equipos_por_ubicacion = list(Equipo.objects.values('ubicacion__nombre')
                               .annotate(total=Count('id'))
                               .values_list('total', flat=True))
    ubicaciones_labels = list(Equipo.objects.values_list('ubicacion__nombre', flat=True).distinct())

    context = {
        'equipos': equipos,
        'categorias': categorias,
        'ubicaciones': ubicaciones,
        'equipos_operativos': equipos_operativos,
        'equipos_mantenimiento': equipos_mantenimiento,
        'equipos_fuera_servicio': equipos_fuera_servicio,
        'equipos_por_categoria': equipos_por_categoria,
        'categorias_labels': categorias_labels,
        'equipos_por_ubicacion': equipos_por_ubicacion,
        'ubicaciones_labels': ubicaciones_labels,
    }
    return render(request, 'equipment/equipo_list.html', context)

@login_required
def ubicacion_list(request):
    ubicaciones = Ubicacion.objects.all()
    
    # Estadísticas
    total_ubicaciones = ubicaciones.count()
    equipos_asignados = Equipo.objects.count()
    ubicaciones_activas = ubicaciones.filter(equipo__isnull=False).distinct().count()
    movimientos_recientes = Movimiento.objects.filter(
        fecha_movimiento__gte=datetime.datetime.now() - datetime.timedelta(days=30)
    ).count()

    # Datos para gráficos
    ubicaciones_nombres = [ub.nombre for ub in ubicaciones]
    equipos_por_ubicacion = [
        Equipo.objects.filter(ubicacion=ub).count()
        for ub in ubicaciones
    ]
    
    movimientos_por_ubicacion = [
        Movimiento.objects.filter(nueva_ubicacion=ub).count()
        for ub in ubicaciones
    ]

    context = {
        'ubicaciones': ubicaciones,
        'total_ubicaciones': total_ubicaciones,
        'equipos_asignados': equipos_asignados,
        'ubicaciones_activas': ubicaciones_activas,
        'movimientos_recientes': movimientos_recientes,
        'ubicaciones_nombres': ubicaciones_nombres,
        'equipos_por_ubicacion': equipos_por_ubicacion,
        'movimientos_por_ubicacion': movimientos_por_ubicacion,
    }
    
    return render(request, 'equipment/ubicacion_list.html', context)

@login_required
def movimiento_list(request):
    movimientos = Movimiento.objects.all()
    equipos = Equipo.objects.all()
    ubicaciones = Ubicacion.objects.all()

    # Estadísticas
    total_movimientos = movimientos.count()
    movimientos_mantenimiento = movimientos.filter(tipo='Mantenimiento').count()
    cambios_ubicacion = movimientos.filter(tipo='Cambio de ubicación').count()
    bajas_equipo = movimientos.filter(tipo='Baja').count()

    # Datos para gráficos
    tipos_movimiento = ['Asignación', 'Cambio de ubicación', 'Mantenimiento', 'Baja']
    movimientos_por_tipo = [
        movimientos.filter(tipo=tipo).count()
        for tipo in tipos_movimiento
    ]

    # Movimientos por mes (últimos 6 meses)
    from django.db.models import Count
    from django.db.models.functions import TruncMonth
    import datetime

    seis_meses_atras = datetime.datetime.now() - datetime.timedelta(days=180)
    movimientos_mensuales = (
        Movimiento.objects
        .filter(fecha_movimiento__gte=seis_meses_atras)
        .annotate(mes=TruncMonth('fecha_movimiento'))
        .values('mes')
        .annotate(total=Count('id'))
        .order_by('mes')
    )

    meses = [m['mes'].strftime('%B') for m in movimientos_mensuales]
    movimientos_por_mes = [m['total'] for m in movimientos_mensuales]

    context = {
        'movimientos': movimientos,
        'equipos': equipos,
        'ubicaciones': ubicaciones,
        'total_movimientos': total_movimientos,
        'movimientos_mantenimiento': movimientos_mantenimiento,
        'cambios_ubicacion': cambios_ubicacion,
        'bajas_equipo': bajas_equipo,
        'tipos_movimiento': tipos_movimiento,
        'movimientos_por_tipo': movimientos_por_tipo,
        'meses': meses,
        'movimientos_por_mes': movimientos_por_mes,
    }
    
    return render(request, 'equipment/movimiento_list.html', context)

@login_required
def equipo_create(request):
    if request.method == 'POST':
        try:
            # Create new equipment
            equipo = Equipo.objects.create(
                nombre=request.POST['nombre'],
                descripcion=request.POST['descripcion'],
                numero_serie=request.POST['numero_serie'],
                marca=request.POST['marca'],
                modelo=request.POST['modelo'],
                categoria_id=request.POST['categoria'],
                ubicacion_id=request.POST['ubicacion'],
                fecha_adquisicion=request.POST['fecha_adquisicion'],
                fecha_garantia=request.POST['fecha_garantia'],
                fecha_expericion=request.POST['fecha_expericion'],
                estado=request.POST['estado']
            )
            messages.success(request, 'Equipo creado exitosamente')
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

@login_required
def equipo_update(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    if request.method == 'POST':
        try:
            # Update equipment
            equipo.nombre = request.POST['nombre']
            equipo.descripcion = request.POST['descripcion']
            equipo.numero_serie = request.POST['numero_serie']
            equipo.marca = request.POST['marca']
            equipo.modelo = request.POST['modelo']
            equipo.categoria_id = request.POST['categoria']
            equipo.ubicacion_id = request.POST['ubicacion']
            equipo.fecha_adquisicion = request.POST['fecha_adquisicion']
            equipo.fecha_garantia = request.POST['fecha_garantia']
            equipo.fecha_expericion = request.POST['fecha_expericion']
            equipo.estado = request.POST['estado']
            equipo.save()
            messages.success(request, 'Equipo actualizado exitosamente')
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

@login_required
def equipo_delete(request, pk):
    if request.method == 'POST':
        try:
            equipo = get_object_or_404(Equipo, pk=pk)
            equipo.delete()
            messages.success(request, 'Equipo eliminado exitosamente')
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

@login_required
def ubicacion_create(request):
    if request.method == 'POST':
        try:
            nueva_ubicacion = Ubicacion.objects.create(
                nombre=request.POST['nombre'],
                descripcion=request.POST['descripcion']
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Ubicación creada exitosamente',
                'id': nueva_ubicacion.id
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    return JsonResponse({
        'status': 'error',
        'message': 'Método no permitido'
    })
