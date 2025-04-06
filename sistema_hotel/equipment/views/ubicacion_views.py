from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import datetime
import json
from ..models import Ubicacion, Equipo, Movimiento

@login_required
def ubicacion_list(request):
    ubicaciones = Ubicacion.objects.all()
    
    # Statistics remain the same
    total_ubicaciones = ubicaciones.count()
    equipos_asignados = Equipo.objects.count()
    ubicaciones_activas = ubicaciones.filter(equipo__isnull=False).distinct().count()
    movimientos_recientes = Movimiento.objects.filter(
        fecha_movimiento__gte=datetime.datetime.now() - datetime.timedelta(days=30)
    ).count()

    # Chart data with proper JSON serialization
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
        'ubicaciones_nombres': json.dumps(ubicaciones_nombres),
        'equipos_por_ubicacion': json.dumps(equipos_por_ubicacion),
        'movimientos_por_ubicacion': json.dumps(movimientos_por_ubicacion),
    }
    
    return render(request, 'equipment/ubicacion_list.html', context)

@login_required
def ubicacion_create(request):
    if request.method == 'POST':
        try:
            ubicacion = Ubicacion.objects.create(
                nombre=request.POST['nombre'],
                descripcion=request.POST['descripcion']
            )
            return JsonResponse({'status': 'success', 'message': 'Ubicación creada exitosamente'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

@login_required
def ubicacion_update(request, pk):
    ubicacion = get_object_or_404(Ubicacion, pk=pk)
    if request.method == 'POST':
        try:
            ubicacion.nombre = request.POST['nombre']
            ubicacion.descripcion = request.POST['descripcion']
            ubicacion.save()
            return JsonResponse({'status': 'success', 'message': 'Ubicación actualizada exitosamente'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

@login_required
def ubicacion_delete(request, pk):
    if request.method == 'POST':
        try:
            ubicacion = get_object_or_404(Ubicacion, pk=pk)
            ubicacion.delete()
            return JsonResponse({'status': 'success', 'message': 'Ubicación eliminada exitosamente'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})


@login_required
def ubicacion_detail(request, pk):
    try:
        ubicacion = get_object_or_404(Ubicacion, pk=pk)
        return JsonResponse({
            'status': 'success',
            'id': ubicacion.id,
            'nombre': ubicacion.nombre,
            'descripcion': ubicacion.descripcion
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })