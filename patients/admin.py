from django.contrib import admin
from django.contrib import messages
from .models import Patient
# You can remove the unused 'from core.models import User' if it was present

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    # This is an assumed working version of your PatientAdmin
    list_display = ['get_username', 'get_full_name', 'blood_group', 'emergency_contact_name', 'is_active']
    list_filter = ['is_active', 'blood_group']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    
    actions = ['delete_selected', 'deactivate_patients', 'activate_patients']
    
    # Custom deletion logic is crucial to also delete the related User
    def has_delete_permission(self, request, obj=None):
        """Allow superusers to delete patients"""
        # Allowing staff to delete the patient here will trigger the User deletion below
        return request.user.is_staff or request.user.is_superuser
    
    def delete_queryset(self, request, queryset):
        """Custom delete for multiple objects - also deletes associated user"""
        count = queryset.count()
        # Collect users to delete first
        users_to_delete = [patient.user for patient in queryset]
        
        # Delete patients (this is not strictly needed if CASCADE is set, but explicit is cleaner)
        queryset.delete()
        
        # Delete associated users (this is needed to clean up the main account)
        for user in users_to_delete:
            user.delete()
            
        self.message_user(request, f'{count} patient(s) and their user account(s) deleted successfully.', messages.SUCCESS)
    
    def delete_model(self, request, obj):
        """Custom delete for single object - also deletes associated user"""
        username = obj.user.username
        user = obj.user
        obj.delete()
        user.delete()  # Delete the associated user account
        self.message_user(request, f'Patient "{username}" and their user account deleted successfully.', messages.SUCCESS)
    
    # Custom actions
    def deactivate_patients(self, request, queryset):
        """Deactivate selected patients"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} patient(s) deactivated successfully.', messages.SUCCESS)
    deactivate_patients.short_description = 'Deactivate selected patients'
    
    def activate_patients(self, request, queryset):
        """Activate selected patients"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} patient(s) activated successfully.', messages.SUCCESS)
    activate_patients.short_description = 'Activate selected patients'
    
    # Custom display methods
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Full Name'
    get_full_name.admin_order_field = 'user__first_name'
