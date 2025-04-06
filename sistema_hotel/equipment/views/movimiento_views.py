from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
import datetime
import json
from ..models import Movimiento, Equipo, Ubicacion

@login_required
def movimiento_list(request):
    movimientos = Movimiento.objects.all()
    equipos = Equipo.objects.all()
    ubicaciones = Ubicacion.objects.all()

    # Statistics remain the same
    total_movimientos = movimientos.count()
    movimientos_mantenimiento = movimientos.filter(tipo='Mantenimiento').count()
    cambios_ubicacion = movimientos.filter(tipo='Cambio de ubicación').count()
    bajas_equipo = movimientos.filter(tipo='Baja').count()

    # Chart data with proper JSON serialization
    tipos_movimiento = ['Asignación', 'Cambio de ubicación', 'Mantenimiento', 'Baja']
    movimientos_por_tipo = [
        movimientos.filter(tipo=tipo).count()
        for tipo in tipos_movimiento
    ]

    # Monthly movements (last 6 months)
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
        'tipos_movimiento': json.dumps(tipos_movimiento),
        'movimientos_por_tipo': json.dumps(movimientos_por_tipo),
        'meses': json.dumps(meses),
        'movimientos_por_mes': json.dumps(movimientos_por_mes),
    }
    
    return render(request, 'equipment/movimiento_list.html', context)

@login_required
def movimiento_create(request):
    if request.method == 'POST':
        try:
            movimiento = Movimiento.objects.create(
                equipo_id=request.POST['equipo'],
                tipo=request.POST['tipo'],
                descripcion=request.POST['descripcion'],
                # Remove usuario_responsable
                nueva_ubicacion_id=request.POST.get('nueva_ubicacion')
            )
            return JsonResponse({'status': 'success', 'message': 'Movimiento creado exitosamente'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

@login_required
def movimiento_update(request, pk):
    movimiento = get_object_or_404(Movimiento, pk=pk)
    if request.method == 'POST':
        try:
            movimiento.equipo_id = request.POST['equipo']
            movimiento.tipo = request.POST['tipo']
            movimiento.descripcion = request.POST['descripcion']
            # Remove the usuario_responsable assignment
            movimiento.nueva_ubicacion_id = request.POST.get('nueva_ubicacion')
            movimiento.save()
            return JsonResponse({'status': 'success', 'message': 'Movimiento actualizado exitosamente'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

@login_required
def movimiento_delete(request, pk):
    if request.method == 'POST':
        try:
            movimiento = get_object_or_404(Movimiento, pk=pk)
            movimiento.delete()
            return JsonResponse({'status': 'success', 'message': 'Movimiento eliminado exitosamente'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})


@login_required
def movimiento_detail(request, pk):
    try:
        movimiento = get_object_or_404(Movimiento, pk=pk)
        return JsonResponse({
            'id': movimiento.id,
            'equipo': movimiento.equipo_id,
            'tipo': movimiento.tipo,
            'descripcion': movimiento.descripcion,
            'nueva_ubicacion': movimiento.nueva_ubicacion_id if movimiento.nueva_ubicacion else '',
            'status': 'success'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })