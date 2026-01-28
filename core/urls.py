from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views

urlpatterns = [
    # ------------------------------------------------------------------
    # Home Page
    # ------------------------------------------------------------------
    path('', views.home, name='home'),
    
    # ------------------------------------------------------------------
    # Authentication (Custom)
    # ------------------------------------------------------------------
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register_view, name='register'),

    # ------------------------------------------------------------------
    # Dashboard & Profile
    # ------------------------------------------------------------------
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),  # Added line

    # ------------------------------------------------------------------
    # Notifications
    # ------------------------------------------------------------------
    path('notifications/', views.notification_list, name='notification_list'),

    # ------------------------------------------------------------------
    # Password Management (fix for NoReverseMatch)
    # ------------------------------------------------------------------
    path('accounts/password_change/', 
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), 
         name='password_change'),
    path('accounts/password_change/done/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
         name='password_change_done'),

    # ------------------------------------------------------------------
    # Admin
    # ------------------------------------------------------------------
    path('admin/', admin.site.urls),
]
