from django.urls import path
from . import views

app_name = 'equipment'

urlpatterns = [
    path('equipos/', views.equipo_list, name='equipo_list'),
    path('ubicaciones/', views.ubicacion_list, name='ubicacion_list'),
    path('movimientos/', views.movimiento_list, name='movimiento_list'),
    path('equipo/create/', views.equipo_create, name='equipo_create'),
    path('equipo/update/<int:pk>/', views.equipo_update, name='equipo_update'),
    path('equipo/delete/<int:pk>/', views.equipo_delete, name='equipo_delete'),
]