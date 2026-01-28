from django.contrib import admin
from django.urls import path, include, reverse_lazy # 👈 Ensure reverse_lazy is imported
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 🔴 FIX 1: Explicitly define the Admin Logout override.
    # Setting next_page to 'admin:login' ensures the "Log in again" link on 
    # the logged out confirmation page points to the Admin Login page.
    path(
        'admin/logout/', 
        auth_views.LogoutView.as_view(
            next_page=reverse_lazy('admin:logout') # 👈 Use the named Admin Login URL
        ),
        name='admin_logout'
    ),

    # Built-in Admin URLs
    path('admin/', admin.site.urls),
    
    # Core App URLs (Home, Register, Dashboard, etc.)
    path('', include('core.urls')), 
    
    # App-specific URLs
    path('patients/', include('patients.urls')),
    path('doctors/', include('doctors.urls')),
    path('appointments/', include('appointments.urls')),
    
    # FIX 2: Regular user logout.
    # This uses LOGOUT_REDIRECT_URL (set to '/') from settings.py.
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    # Serve media files only during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
