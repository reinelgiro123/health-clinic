from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # BaseUserAdmin is used here as a convention, but your provided code used UserAdmin
from django.contrib import messages
from django.db import transaction # Essential for atomic deletion

# Import necessary profile models
from .models import User
from patients.models import Patient 
from doctors.models import Doctor # Assumed to be available for related deletion


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    # --- LIST DISPLAY & FILTERS (Using your provided list) ---
    # We must use BaseUserAdmin.list_display to inherit Django's core fields, 
    # but we'll include your custom fields like 'role' from your User model.
    list_display = ['username', 'email', 'role', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_patient', 'is_doctor']
    list_filter = ['role', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['-date_joined']
    
    # Enable deletion and custom actions
    actions = ['delete_selected', 'deactivate_users', 'activate_users']

    # --- FIELDSETS (Using your provided fieldsets) ---
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'date_of_birth', 'address', 'profile_picture')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'email', 'first_name', 'last_name', 'phone')
        }),
    )
    
    # --- PERMISSIONS & CUSTOM ACTIONS (Using your provided actions) ---
    def has_delete_permission(self, request, obj=None):
        """Allow superusers to delete users"""
        return request.user.is_superuser
    
    # Custom actions
    def deactivate_users(self, request, queryset):
        """Deactivate selected users instead of deleting (soft-delete)"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} user(s) deactivated successfully.', messages.SUCCESS)
    deactivate_users.short_description = 'Deactivate selected users'
    
    def activate_users(self, request, queryset):
        """Activate selected users"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} user(s) activated successfully.', messages.SUCCESS)
    activate_users.short_description = 'Activate selected users'

    # --- PROFILE DELETION LOGIC (CRITICAL FIX) ---
    
    def delete_related_profiles(self, user):
        """Helper to explicitly delete all related profile models before the User."""
        # 1. Delete Patient Profile
        try:
            # Use the related_name 'patient_profile'
            user.patient_profile.delete()
        except Patient.DoesNotExist:
            pass
        
        # 2. Delete Doctor Profile
        try:
            # Assuming the Doctor model uses the related_name 'doctor_profile'
            user.doctor_profile.delete()
        except Doctor.DoesNotExist:
            pass
        # Add other related profile deletions here if necessary


    @transaction.atomic # CRITICAL: Ensures all deletions happen together in the DB
    def delete_model(self, request, obj):
        """Custom delete for single User: deletes related profiles first, then the User."""
        self.delete_related_profiles(obj)
        
        # Now delete the user
        super().delete_model(request, obj)
        self.message_user(request, f'User "{obj.username}" and all related profiles deleted successfully.', messages.SUCCESS)

    @transaction.atomic # CRITICAL: Ensures all deletions happen together in the DB
    def delete_queryset(self, request, queryset):
        """Custom delete for multiple Users: deletes related profiles first, then the Users."""
        count = queryset.count()
        for user in queryset:
            self.delete_related_profiles(user)

        # Now delete the queryset of users
        super().delete_queryset(request, queryset)
        self.message_user(request, f'{count} user(s) and all related profiles deleted successfully.', messages.SUCCESS)

    # --- CUSTOM DISPLAY METHODS FOR LIST_DISPLAY ---
    def is_patient(self, obj):
        """Check if the user has an associated patient profile."""
        return hasattr(obj, 'patient_profile')
    is_patient.boolean = True
    is_patient.short_description = 'Patient'
    
    def is_doctor(self, obj):
        """Check if the user has an associated doctor profile."""
        return hasattr(obj, 'doctor_profile')
    is_doctor.boolean = True
    is_doctor.short_description = 'Doctor'
