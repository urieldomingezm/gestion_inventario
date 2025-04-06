from django.contrib import admin
from django.urls import path, include
from accounts.views import login_view, register_view, home_view
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_login, name='root'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),
    path('equipment/', include(('equipment.urls', 'equipment'), namespace='equipment')),  # Updated this line
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
