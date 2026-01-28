from django.contrib import admin
from django.contrib import messages
from core.models import User # Import User from the 'core' app
from .models import Doctor, DoctorSchedule

# =========================================================================
# 1. Doctor Admin
# =========================================================================

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'get_full_name', 'specialization', 'license_number', 'years_of_experience', 'is_available', 'rating']
    list_filter = ['specialization', 'is_available']
    search_fields = ['user__username', 'user__email', 'specialization', 'license_number']
    
    actions = ['delete_selected', 'mark_available', 'mark_unavailable']
    
    def has_delete_permission(self, request, obj=None):
        """Allow superusers to delete doctors"""
        return request.user.is_superuser
    
    def delete_queryset(self, request, queryset):
        """Custom delete for multiple objects - also deletes associated user"""
        count = queryset.count()
        # Collect users to delete first
        users_to_delete = [doctor.user for doctor in queryset]
        
        # Delete doctors
        queryset.delete()
        
        # Delete associated users
        for user in users_to_delete:
            user.delete()
            
        self.message_user(request, f'{count} doctor(s) and their user account(s) deleted successfully.', messages.SUCCESS)
    
    def delete_model(self, request, obj):
        """Custom delete for single object - also deletes associated user"""
        username = obj.user.username
        user = obj.user
        obj.delete()
        user.delete()  # Delete the associated user account
        self.message_user(request, f'Doctor "{username}" and their user account deleted successfully.', messages.SUCCESS)
    
    # Custom actions
    def mark_available(self, request, queryset):
        """Mark selected doctors as available"""
        updated = queryset.update(is_available=True)
        self.message_user(request, f'{updated} doctor(s) marked as available.', messages.SUCCESS)
    mark_available.short_description = 'Mark as Available'
    
    def mark_unavailable(self, request, queryset):
        """Mark selected doctors as unavailable"""
        updated = queryset.update(is_available=False)
        self.message_user(request, f'{updated} doctor(s) marked as unavailable.', messages.SUCCESS)
    mark_unavailable.short_description = 'Mark as Unavailable'
    
    # Custom display methods
    def get_username(self, obj):
        # Retrieve the username from the related User model
        return obj.user.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'
    
    def get_full_name(self, obj):
        # Retrieve the full name from the related User model
        return obj.user.get_full_name() or '-'
    get_full_name.short_description = 'Full Name'
    get_full_name.admin_order_field = 'user__first_name'

# =========================================================================
# 2. DoctorSchedule Admin
# =========================================================================

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'get_day', 'start_time', 'end_time', 'is_active']
    list_filter = ['day_of_week', 'is_active']
    search_fields = ['doctor__user__username', 'doctor__specialization']
    
    actions = ['delete_selected', 'activate_schedules', 'deactivate_schedules']
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion of schedules by staff users (Admins, Doctors)"""
        return request.user.is_staff
    
    def delete_queryset(self, request, queryset):
        """Custom delete for multiple schedules"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} schedule(s) deleted successfully.', messages.SUCCESS)
    
    # Custom actions
    def activate_schedules(self, request, queryset):
        """Activate selected schedules"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} schedule(s) activated.', messages.SUCCESS)
    activate_schedules.short_description = 'Activate selected schedules'
    
    def deactivate_schedules(self, request, queryset):
        """Deactivate selected schedules"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} schedule(s) deactivated.', messages.SUCCESS)
    deactivate_schedules.short_description = 'Deactivate selected schedules'
    
    # Custom display methods
    def get_day(self, obj):
        # Uses Django's built-in display method for CharField/IntegerField with choices
        return obj.get_day_of_week_display()
    get_day.short_description = 'Day'
    get_day.admin_order_field = 'day_of_week'
