from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import time, datetime
from django.core.mail import send_mail
from django.conf import settings
from .models import Appointment


# ✅ CANCEL APPOINTMENT
@login_required
def cancel_appointment(request, appointment_id):
    """Cancel an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # ✅ Allow only the patient or admin/doctor to cancel
    if request.user.role == 'patient' and appointment.patient.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('my_appointments')

    if appointment.status in ['pending', 'confirmed']:
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled successfully!')

        # ✅ Send email notification
        message = (
            f"Your appointment with Dr. {appointment.doctor.get_full_name()} "
            f"on {appointment.appointment_date} at {appointment.appointment_time} "
            f"has been cancelled."
        )
        send_mail(
            subject="Clinic Appointment Cancelled",
            message=f"Dear {appointment.patient.get_full_name()},\n\n{message}\n\nThank you!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.patient.email],
            fail_silently=True,  # prevent crash if email not configured
        )
    else:
        messages.error(request, 'Cannot cancel this appointment.')

    return redirect('my_appointments')


# ✅ RESCHEDULE APPOINTMENT
@login_required
def reschedule_appointment(request, appointment_id):
    """Reschedule an appointment with validation for date and time"""
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # ✅ Only patient who booked or admin/doctor can reschedule
    if request.user.role == 'patient' and appointment.patient.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('my_appointments')

    if request.method == 'POST':
        new_date = request.POST.get('appointment_date')
        new_time = request.POST.get('appointment_time')

        # ✅ Validate date and time format
        try:
            selected_date = datetime.strptime(new_date, '%Y-%m-%d').date()
            selected_time = datetime.strptime(new_time, '%H:%M').time()
        except (ValueError, TypeError):
            messages.error(request, 'Invalid date or time format.')
            return redirect('reschedule_appointment', appointment_id=appointment.id)

        today = timezone.now().date()

        # ✅ Restriction 1: Prevent selecting past dates
        if selected_date < today:
            messages.error(request, 'You cannot choose a past date.')
            return redirect('reschedule_appointment', appointment_id=appointment.id)

        # ✅ Restriction 2: Allow time only between 7AM and 7PM
        if selected_time < time(7, 0) or selected_time > time(19, 0):
            messages.error(request, 'Appointments are only available from 7:00 AM to 7:00 PM.')
            return redirect('reschedule_appointment', appointment_id=appointment.id)

        # ✅ Check if the new slot is already booked
        existing = Appointment.objects.filter(
            doctor=appointment.doctor,
            appointment_date=selected_date,
            appointment_time=selected_time
        ).exclude(id=appointment_id).exclude(status='cancelled').exists()

        if existing:
            messages.error(request, 'This time slot is already booked.')
        else:
            appointment.appointment_date = selected_date
            appointment.appointment_time = selected_time
            appointment.status = 'pending'  # mark as pending again
            appointment.save()
            messages.success(request, 'Appointment rescheduled successfully!')

            # ✅ Send email notification
            message = (
                f"Your appointment has been rescheduled to "
                f"{appointment.appointment_date} at {appointment.appointment_time} "
                f"with Dr. {appointment.doctor.get_full_name()}."
            )
            send_mail(
                subject="Clinic Appointment Rescheduled",
                message=f"Dear {appointment.patient.get_full_name()},\n\n{message}\n\nThank you!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[appointment.patient.email],
                fail_silently=True,
            )

            return redirect('my_appointments')

    context = {
        'appointment': appointment,
        'today': timezone.now().date(),  # 👈 for min date in HTML input
    }
    return render(request, 'appointments/reschedule.html', context)


# ✅ APPROVE APPOINTMENT
@login_required
def approve_appointment(request, appointment_id):
    """Doctor or admin approves a pending appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user.role not in ['doctor', 'admin']:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    if appointment.status != 'pending':
        messages.error(request, 'Only pending appointments can be approved.')
        return redirect('doctor_dashboard')

    appointment.status = 'confirmed'
    appointment.save()
    messages.success(request, 'Appointment approved successfully!')

    # ✅ Send email notification
    message = (
        f"Your appointment with Dr. {appointment.doctor.get_full_name()} "
        f"on {appointment.appointment_date} at {appointment.appointment_time} has been approved."
    )
    send_mail(
        subject="Clinic Appointment Approved",
        message=f"Dear {appointment.patient.get_full_name()},\n\n{message}\n\nThank you!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[appointment.patient.email],
        fail_silently=True,
    )

    return redirect('doctor_dashboard')


# ✅ REJECT APPOINTMENT
@login_required
def reject_appointment(request, appointment_id):
    """Doctor or admin rejects an appointment"""
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user.role not in ['doctor', 'admin']:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')

    if appointment.status not in ['pending', 'confirmed']:
        messages.error(request, 'Only pending or confirmed appointments can be rejected.')
        return redirect('doctor_dashboard')

    appointment.status = 'rejected'
    appointment.save()
    messages.success(request, 'Appointment rejected successfully.')

    # ✅ Send email notification
    message = (
        f"Your appointment with Dr. {appointment.doctor.get_full_name()} "
        f"on {appointment.appointment_date} at {appointment.appointment_time} has been rejected."
    )
    send_mail(
        subject="Clinic Appointment Rejected",
        message=f"Dear {appointment.patient.get_full_name()},\n\n{message}\n\nThank you!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[appointment.patient.email],
        fail_silently=True,
    )

    return redirect('doctor_dashboard')
