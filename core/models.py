from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

# -----------------------------
# Custom User Model (FIXED)
# -----------------------------
class User(AbstractUser):
    """Extended User model with role-based access"""
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    phone = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 🔴 FIX E304: Add unique related_name arguments to inherited fields
    # This prevents clashes with the default auth.User model's reverse accessors.
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=('The groups this user belongs to.'),
        related_name="core_user_set", # UNIQUE NAME
        related_query_name="core_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="core_user_permissions_set", # UNIQUE NAME
        related_query_name="core_user_permission",
    )
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# -----------------------------
# Appointment Model (No changes needed for core app errors)
# -----------------------------
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('rescheduled', 'Rescheduled'),
        ('completed', 'Completed'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_appointments")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_appointments")
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.patient.username} - {self.date.strftime('%Y-%m-%d %H:%M')} ({self.status})"


# -----------------------------
# Notification Model (No changes needed for core app errors)
# -----------------------------
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} → {self.recipient.username}"