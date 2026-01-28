from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction  # Needed for atomic saving in edit_profile
from .form import (
    UserRegistrationForm, PatientRegistrationForm, DoctorRegistrationForm,
    UserUpdateForm, PatientUpdateForm, DoctorUpdateForm
) 
from patients.models import Patient
from doctors.models import Doctor

# -----------------------------
# Home and Authentication Views
# -----------------------------
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'pages/home.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next') or 'dashboard'
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'pages/login.html', {'next': request.GET.get('next', '')})


def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, request.FILES)
        patient_form = PatientRegistrationForm(request.POST)
        doctor_form = DoctorRegistrationForm(request.POST)
        role = request.POST.get('role', 'patient')
        
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.role = role
            user.save()

            if role == 'patient' and patient_form.is_valid():
                data = patient_form.cleaned_data
                Patient.objects.create(
                    user=user,
                    blood_group=data.get('blood_group', ''),
                    medical_history=data.get('medical_history', ''),
                    emergency_contact_name=data.get('emergency_contact_name', ''),
                    emergency_contact_phone=data.get('emergency_contact_phone', ''),
                )
            elif role == 'doctor' and doctor_form.is_valid():
                data = doctor_form.cleaned_data
                Doctor.objects.create(
                    user=user,
                    specialization=data.get('specialization', ''),
                    license_number=data.get('license_number', ''),
                    years_of_experience=data.get('years_of_experience', 0),
                    consultation_fee=data.get('consultation_fee', 0),
                    bio=data.get('bio', ''),
                )
            else:
                messages.error(request, 'Please fill in all required profile fields.')
                return render(request, 'pages/register.html', {
                    'user_form': user_form,
                    'patient_form': patient_form,
                    'doctor_form': doctor_form,
                })

            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')

    else:
        user_form = UserRegistrationForm()
        patient_form = PatientRegistrationForm()
        doctor_form = DoctorRegistrationForm()
    
    return render(request, 'pages/register.html', {
        'user_form': user_form,
        'patient_form': patient_form,
        'doctor_form': doctor_form,
    })


# -----------------------------
# Dashboard Redirect Logic
# -----------------------------
@login_required
def dashboard(request):
    """Redirect users to their respective dashboards based on role"""
    user = request.user

    if user.is_superuser:
        # Ensure role is set to avoid redirect loops
        if user.role != 'doctor':
            user.role = 'doctor'
            user.save()
            
        # Use defaults to satisfy the UNIQUE constraint on license_number
        Doctor.objects.get_or_create(
            user=user,
            defaults={
                'license_number': f"ADMIN-{user.id}", # Unique placeholder
                'specialization': 'Administrator',
            }
        )
        return redirect('doctor_dashboard')

    if getattr(user, 'role', None) == 'patient':
        Patient.objects.get_or_create(user=user)
        return redirect('patient_dashboard')
        
    elif getattr(user, 'role', None) == 'doctor':
        Doctor.objects.get_or_create(user=user)
        return redirect('doctor_dashboard')

    return redirect('home')
# -----------------------------
# Notifications
# -----------------------------
@login_required
def notification_list(request):
    notifications = []  # Placeholder
    return render(request, 'core/notifications.html', {'notifications': notifications})


# -----------------------------
# Profile Editing
# -----------------------------
@login_required
@transaction.atomic
def edit_profile(request):
    profile_instance = None
    profile_form_class = None
    
    if hasattr(request.user, 'patient'):
        profile_instance = request.user.patient
        profile_form_class = PatientUpdateForm
    elif hasattr(request.user, 'doctor'):
        profile_instance = request.user.doctor
        profile_form_class = DoctorUpdateForm

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = profile_form_class(request.POST, instance=profile_instance) if profile_form_class else None

        user_form_valid = user_form.is_valid()
        profile_form_valid = profile_form.is_valid() if profile_form else True
        
        if user_form_valid and profile_form_valid:
            user_form.save()
            if profile_form:
                profile_form.save()
            
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('dashboard')
        else:
            if profile_form:
                 profile_form = profile_form_class(request.POST, instance=profile_instance)
            messages.error(request, 'Please correct the errors below.')
    
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = profile_form_class(instance=profile_instance) if profile_form_class else None

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_patient': hasattr(request.user, 'patient'),
        'is_doctor': hasattr(request.user, 'doctor'),
    }
    
    return render(request, 'core/edit_profile.html', context)


# -----------------------------
# Password Change
# -----------------------------
@login_required
def change_password(request):
    """Change user password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'core/change_password.html', {'form': form})
