from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/edit_profile/', views.edit_profile, name='patient_edit_profile'),
    path('appointments/', views.my_appointments, name='my_appointments'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('profile/', views.patient_profile, name='patient_profile'),
]
