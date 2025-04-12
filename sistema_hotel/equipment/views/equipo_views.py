from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from ..models import Equipo, Categoria, Ubicacion
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def equipo_list(request):
    equipos = Equipo.objects.all()
    categorias = Categoria.objects.all()
    ubicaciones = Ubicacion.objects.all()
    
    # Statistics
    equipos_operativos = equipos.filter(estado='Operativo').count()
    equipos_mantenimiento = equipos.filter(estado='En mantenimiento').count()
    equipos_fuera_servicio = equipos.filter(estado='Fuera de servicio').count()

    # Chart data
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
def equipo_detail(request, pk):
    try:
        equipo = get_object_or_404(Equipo, pk=pk)
        return JsonResponse({
            'id': equipo.id,
            'nombre': equipo.nombre,
            'numero_serie': equipo.numero_serie,
            'categoria': equipo.categoria_id,
            'estado': equipo.estado,
            'ubicacion': equipo.ubicacion_id,
            'status': 'success'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@login_required
def equipo_create(request):
    if request.method == 'POST':
        try:
            equipo = Equipo.objects.create(
                nombre=request.POST['nombre'],
                numero_serie=request.POST['numero_serie'],
                categoria_id=request.POST['categoria'],
                estado=request.POST['estado'],
                ubicacion_id=request.POST['ubicacion']
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Equipo creado exitosamente'
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

@login_required
def equipo_update(request, pk):
    equipo = get_object_or_404(Equipo, pk=pk)
    if request.method == 'POST':
        try:
            equipo.nombre = request.POST['nombre']
            equipo.numero_serie = request.POST['numero_serie']
            equipo.categoria_id = request.POST['categoria']
            equipo.estado = request.POST['estado']
            equipo.ubicacion_id = request.POST['ubicacion']
            equipo.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Equipo actualizado exitosamente'
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

@login_required
def equipo_delete(request, pk):
    if request.method == 'POST':
        try:
            equipo = get_object_or_404(Equipo, pk=pk)
            equipo.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Equipo eliminado exitosamente'
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


@csrf_exempt
def import_excel(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            equipos = data.get('equipos', [])
            
            for equipo_data in equipos:
                # Get or create categoria and ubicacion by name
                categoria_nombre = equipo_data.get('categoria')
                ubicacion_nombre = equipo_data.get('ubicacion')
                
                try:
                    categoria = Categoria.objects.get(nombre=categoria_nombre)
                except Categoria.DoesNotExist:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Categoría no encontrada: {categoria_nombre}'
                    })
                
                try:
                    ubicacion = Ubicacion.objects.get(nombre=ubicacion_nombre)
                except Ubicacion.DoesNotExist:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Ubicación no encontrada: {ubicacion_nombre}'
                    })
                
                # Create the equipment
                Equipo.objects.create(
                    nombre=equipo_data.get('nombre'),
                    numero_serie=equipo_data.get('numero_serie'),
                    categoria=categoria,
                    estado=equipo_data.get('estado'),
                    ubicacion=ubicacion
                )
            
            return JsonResponse({
                'status': 'success',
                'message': f'Se importaron {len(equipos)} equipos correctamente'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Error al decodificar JSON'
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