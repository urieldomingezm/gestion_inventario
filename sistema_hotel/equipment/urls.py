from django.urls import path
from .views import equipo_views, ubicacion_views, movimiento_views

app_name = 'equipment'

urlpatterns = [
    # Equipment URLs
    path('equipos/', equipo_views.equipo_list, name='equipo_list'),
    path('equipo/create/', equipo_views.equipo_create, name='equipo_create'),
    path('equipo/<int:pk>/', equipo_views.equipo_detail, name='equipo_detail'),
    path('equipo/update/<int:pk>/', equipo_views.equipo_update, name='equipo_update'),
    path('equipo/delete/<int:pk>/', equipo_views.equipo_delete, name='equipo_delete'),
    path('import-excel/', equipo_views.import_excel, name='import_excel'),

    # Location URLs
    path('ubicaciones/', ubicacion_views.ubicacion_list, name='ubicacion_list'),
    path('ubicacion/<int:pk>/', ubicacion_views.ubicacion_detail, name='ubicacion_detail'),
    path('ubicacion/create/', ubicacion_views.ubicacion_create, name='ubicacion_create'),
    path('ubicacion/update/<int:pk>/', ubicacion_views.ubicacion_update, name='ubicacion_update'),
    path('ubicacion/delete/<int:pk>/', ubicacion_views.ubicacion_delete, name='ubicacion_delete'),

    # Movement URLs
    path('movimientos/', movimiento_views.movimiento_list, name='movimiento_list'),
    path('movimiento/create/', movimiento_views.movimiento_create, name='movimiento_create'),
    path('movimiento/update/<int:pk>/', movimiento_views.movimiento_update, name='movimiento_update'),
    path('movimiento/delete/<int:pk>/', movimiento_views.movimiento_delete, name='movimiento_delete'),
    path('movimiento/<int:pk>/', movimiento_views.movimiento_detail, name='movimiento_detail'),
]