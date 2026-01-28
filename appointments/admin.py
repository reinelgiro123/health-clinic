from django.contrib import admin
from django.contrib import messages
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    # Display fields now use custom methods for full names instead of raw IDs
    list_display = ['id', 'get_patient_name', 'get_doctor_name', 'appointment_date', 'appointment_time', 'status', 'created_at']
    list_filter = ['status', 'appointment_date', 'doctor__specialization', 'created_at']
    search_fields = [
        'patient__user__username', 
        'patient__user__email',
        'doctor__user__username', 
        'doctor__specialization',
        'reason'
    ]
    date_hierarchy = 'appointment_date'
    readonly_fields = ['created_at', 'updated_at']
    
    # Custom actions including all status updates and delete
    actions = [
        'delete_selected', 
        'mark_as_confirmed', 
        'mark_as_completed', 
        'mark_as_cancelled',
        'mark_as_pending'
    ]
    
    def has_delete_permission(self, request, obj=None):
        """Allow staff users (Admins, Doctors) to delete appointments"""
        return request.user.is_staff
    
    def delete_queryset(self, request, queryset):
        """Custom delete for multiple appointments"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} appointment(s) deleted successfully.', messages.SUCCESS)
    
    def delete_model(self, request, obj):
        """Custom delete for single appointment"""
        appointment_id = obj.id
        obj.delete()
        self.message_user(request, f'Appointment #{appointment_id} deleted successfully.', messages.SUCCESS)
    
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'doctor', 'appointment_date', 'appointment_time', 'status')
        }),
        ('Additional Information', {
            'fields': ('reason', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # --- Status change actions ---
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} appointment(s) marked as confirmed.', messages.SUCCESS)
    mark_as_confirmed.short_description = 'Mark selected as Confirmed'
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} appointment(s) marked as completed.', messages.SUCCESS)
    mark_as_completed.short_description = 'Mark selected as Completed'
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} appointment(s) marked as cancelled.', messages.SUCCESS)
    mark_as_cancelled.short_description = 'Mark selected as Cancelled'
    
    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} appointment(s) marked as pending.', messages.SUCCESS)
    mark_as_pending.short_description = 'Mark selected as Pending'
    
    # --- Custom display methods ---
    
    def get_patient_name(self, obj):
        # Displays patient's full name, falling back to username
        return obj.patient.user.get_full_name() or obj.patient.user.username
    get_patient_name.short_description = 'Patient'
    get_patient_name.admin_order_field = 'patient__user__first_name'
    
    def get_doctor_name(self, obj):
        # Displays doctor's name prefixed with 'Dr.'
        full_name = obj.doctor.user.get_full_name()
        if full_name:
            return f"Dr. {full_name}"
        return f"Dr. {obj.doctor.user.username}"
    get_doctor_name.short_description = 'Doctor'
    get_doctor_name.admin_order_field = 'doctor__user__first_name'
