from django.urls import path
from . import views

urlpatterns = [
    path('<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('<int:appointment_id>/reschedule/', views.reschedule_appointment, name='reschedule_appointment'),
    path('<int:appointment_id>/approve/', views.approve_appointment, name='approve_appointment'),
    path('<int:appointment_id>/reject/', views.reject_appointment, name='reject_appointment'),
]
