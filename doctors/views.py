from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointments.models import Appointment
from .models import Doctor, DoctorSchedule

@login_required
def doctor_dashboard(request):
    """Doctor dashboard view"""
    if request.user.role != 'doctor':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_date')[:10]
    
    # Statistics
    total_appointments = Appointment.objects.filter(doctor=doctor).count()
    pending = Appointment.objects.filter(doctor=doctor, status='pending').count()
    confirmed = Appointment.objects.filter(doctor=doctor, status='confirmed').count()
    completed = Appointment.objects.filter(doctor=doctor, status='completed').count()
    
    context = {
        'doctor': doctor,
        'appointments': appointments,
        'total_appointments': total_appointments,
        'pending_appointments': pending,
        'confirmed_appointments': confirmed,
        'completed_appointments': completed,
        'cancelled_appointments': Appointment.objects.filter(doctor=doctor, status='cancelled').count(),
    }
    return render(request, 'doctors/organisms/doctor_dashboard.html', context)


@login_required
def doctor_appointments(request):
    """View all doctor appointments"""
    if request.user.role != 'doctor':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    doctor = get_object_or_404(Doctor, user=request.user)
    status_filter = request.GET.get('status', '')
    
    appointments = Appointment.objects.filter(doctor=doctor)
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    
    appointments = appointments.order_by('-appointment_date', '-appointment_time')
    
    context = {
        'appointments': appointments,
        'status_filter': status_filter,
    }
    return render(request, 'doctors/appointments.html', context)


@login_required
def update_appointment_status(request, appointment_id):
    """Update appointment status"""
    if request.user.role != 'doctor':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    doctor = get_object_or_404(Doctor, user=request.user)
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        if new_status in ['confirmed', 'completed', 'rejected']:
            appointment.status = new_status
            if notes:
                appointment.notes = notes
            appointment.save()
            messages.success(request, f'Appointment {new_status} successfully!')
        else:
            messages.error(request, 'Invalid status.')
    
    return redirect('doctor_appointments')


@login_required
def cancel_appointment(request, appointment_id):
    """Cancel an appointment (doctor or patient)"""
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Only doctor of the appointment or the patient who booked it can cancel
    if request.user.role == 'doctor' and appointment.doctor.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('doctor_appointments')
    elif request.user.role == 'patient' and appointment.patient.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('my_appointments')
    
    if appointment.status in ['pending', 'confirmed']:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully!')
    else:
        messages.error(request, 'This appointment cannot be cancelled.')
    
    # Redirect depending on user role
    if request.user.role == 'doctor':
        return redirect('doctor_appointments')
    else:
        return redirect('my_appointments')


@login_required
def doctor_schedule(request):
    """Manage doctor schedule"""
    if request.user.role != 'doctor':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    doctor = get_object_or_404(Doctor, user=request.user)
    schedules = DoctorSchedule.objects.filter(doctor=doctor).order_by('day_of_week', 'start_time')
    
    if request.method == 'POST':
        day_of_week = request.POST.get('day_of_week')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        
        DoctorSchedule.objects.create(
            doctor=doctor,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            is_active=True
        )
        messages.success(request, 'Schedule added successfully!')
        return redirect('doctor_schedule')
    
    context = {
        'schedules': schedules,
    }
    return render(request, 'doctors/schedule.html', context)


@login_required
def reschedule_appointment(request, appointment_id):
    """Reschedule an appointment (doctor or patient)"""
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Allow only doctor or patient who owns the appointment
    if request.user.role == 'doctor' and appointment.doctor.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('doctor_appointments')
    elif request.user.role == 'patient' and appointment.patient.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('my_appointments')

    if request.method == 'POST':
        new_date = request.POST.get('appointment_date')
        new_time = request.POST.get('appointment_time')

        if new_date and new_time:
            appointment.appointment_date = new_date
            appointment.appointment_time = new_time
            appointment.status = 'pending'
            appointment.save()
            messages.success(request, 'Appointment rescheduled successfully!')
            if request.user.role == 'doctor':
                return redirect('doctor_appointments')
            else:
                return redirect('my_appointments')
        else:
            messages.error(request, 'Please select both date and time.')

    context = {
        'appointment': appointment,
    }
    return render(request, 'doctors/reschedule_appointment.html', context)


# 🆕 Doctor Profile View
@login_required
def doctor_profile(request):
    """View and edit doctor profile"""
    if request.user.role != 'doctor':
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    doctor = get_object_or_404(Doctor, user=request.user)
    
    if request.method == 'POST':
        # Update user info
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.phone = request.POST.get('phone')
        request.user.address = request.POST.get('address', '')
        request.user.save()
        
        # Update doctor info
        doctor.specialization = request.POST.get('specialization')
        doctor.years_of_experience = request.POST.get('years_of_experience', 0)
        doctor.consultation_fee = request.POST.get('consultation_fee', 0)
        doctor.bio = request.POST.get('bio', '')
        doctor.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('doctor_profile')
    
    context = {
        'doctor': doctor,
    }
    return render(request, 'doctors/profile.html', context)
