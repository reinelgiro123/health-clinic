from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from appointments.models import Appointment
from doctors.models import Doctor
from .models import Patient


# ------------------------------------------------------------------
# 1️⃣ PATIENT DASHBOARD
# ------------------------------------------------------------------
@login_required
def patient_dashboard(request):
    """Patient dashboard view"""
    if request.user.role != 'patient':
        messages.error(request, 'Access denied.')
        return redirect('home')

    patient = get_object_or_404(Patient, user=request.user)
    all_appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
    appointments = all_appointments[:5]

    total_appointments = all_appointments.count()
    pending = all_appointments.filter(status='pending').count()
    confirmed = all_appointments.filter(status='confirmed').count()
    completed = all_appointments.filter(status='completed').count()
    cancelled = all_appointments.filter(status='cancelled').count()

    context = {
        'patient': patient,
        'appointments': appointments,
        'total_appointments': total_appointments,
        'pending_appointments': pending,
        'confirmed_appointments': confirmed,
        'completed_appointments': completed,
        'cancelled_appointments': cancelled,
    }
    return render(request, 'patients/organisms/patient_dashboard.html', context)


# ------------------------------------------------------------------
# 2️⃣ MY APPOINTMENTS
# ------------------------------------------------------------------
@login_required
def my_appointments(request):
    """View all patient appointments"""
    if request.user.role != 'patient':
        messages.error(request, 'Access denied.')
        return redirect('home')

    patient = get_object_or_404(Patient, user=request.user)
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')

    context = {
        'appointments': appointments,
    }
    return render(request, 'patients/my_appointments.html', context)


# ------------------------------------------------------------------
# 3️⃣ BOOK APPOINTMENT
# ------------------------------------------------------------------
@login_required
def book_appointment(request):
    """Book a new appointment"""
    if request.user.role != 'patient':
        messages.error(request, 'Access denied.')
        return redirect('home')

    patient = get_object_or_404(Patient, user=request.user)
    doctors = Doctor.objects.filter(is_available=True)

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason')

        doctor = get_object_or_404(Doctor, id=doctor_id)
        existing = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exclude(status='cancelled').exists()

        if existing:
            messages.error(request, 'This time slot is already booked.')
        else:
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=reason,
                status='pending'
            )
            messages.success(request, 'Appointment booked successfully!')
            return redirect('my_appointments')

    context = {
        'doctors': doctors,
    }
    return render(request, 'patients/book_appointment.html', context)


# ------------------------------------------------------------------
# 4️⃣ PATIENT PROFILE
# ------------------------------------------------------------------
@login_required
def patient_profile(request):
    """View and edit patient profile"""
    if request.user.role != 'patient':
        messages.error(request, 'Access denied.')
        return redirect('home')

    patient = get_object_or_404(Patient, user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')
        request.user.save()

        patient.blood_group = request.POST.get('blood_group')
        patient.medical_history = request.POST.get('medical_history')
        patient.emergency_contact_name = request.POST.get('emergency_contact_name')
        patient.emergency_contact_phone = request.POST.get('emergency_contact_phone')
        patient.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('patient_profile')

    context = {
        'patient': patient,
    }
    return render(request, 'patients/patient_profile.html', context)


# ------------------------------------------------------------------
# 5️⃣ EDIT PROFILE (USER DETAILS SETTINGS DASHBOARD)
# ------------------------------------------------------------------
@login_required
def edit_profile(request):
    """
    Display and update the patient's profile and user details.
    """
    if request.user.role != 'patient':
        messages.error(request, 'Access denied. Only patients can edit this profile.')
        return redirect('home')

    patient = get_object_or_404(Patient, user=request.user)

    if request.method == 'POST':
        # Update User fields
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()

        # Update Patient fields
        patient.phone = request.POST.get('phone', patient.phone)
        patient.blood_group = request.POST.get('blood_group', patient.blood_group)
        patient.medical_history = request.POST.get('medical_history', patient.medical_history)
        patient.save()

        messages.success(request, 'Your profile has been successfully updated.')
        return redirect('edit_profile')

    context = {
        'user': request.user,
        'patient': patient,
    }
    return render(request, 'patients/edit_profile.html', context)
