from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from equipment.models import Equipo, Movimiento, Ubicacion

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo ya está registrado')
            return redirect('register')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        messages.success(request, 'Registro exitoso')
        login(request, user)
        return redirect('home')
    
    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Bienvenido')
            return redirect('home')
        else:
            messages.error(request, 'Credenciales inválidas')
    
    return render(request, 'accounts/login.html')

def home_view(request):
    # Equipment statistics by category
    equipos_por_categoria = Equipo.objects.values('categoria__nombre').annotate(total=Count('id'))
    
    # Equipment statistics by status
    equipos_por_estado = Equipo.objects.values('estado').annotate(total=Count('id'))
    
    # Equipment by location
    equipos_por_ubicacion = Equipo.objects.values('ubicacion__nombre').annotate(total=Count('id'))
    
    # Recent movements
    movimientos_recientes = Movimiento.objects.select_related('equipo').order_by('-fecha_movimiento')[:5]

    context = {
        'equipos_por_categoria': list(equipos_por_categoria),
        'equipos_por_estado': list(equipos_por_estado),
        'equipos_por_ubicacion': list(equipos_por_ubicacion),
        'movimientos_recientes': movimientos_recientes,
    }
    return render(request, 'accounts/home.html', context)
