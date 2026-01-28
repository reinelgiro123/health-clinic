from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('appointment/<int:appointment_id>/update/', views.update_appointment_status, name='update_appointment_status'),
    path('schedule/', views.doctor_schedule, name='doctor_schedule'),
    path('profile/', views.doctor_profile, name='doctor_profile'),  # Added line
    path('appointment/<int:appointment_id>/reschedule/', views.reschedule_appointment, name='reschedule_appointment'),
    path('appointment/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
]
