from django.db import models
from django.conf import settings


# -----------------------------
# Doctor Model
# -----------------------------
class Doctor(models.Model):
    """Doctor profile with specialization, license, and availability."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # ✅ ensures deletion cascade
        related_name='doctor_profile',
        help_text="Linked user account for the doctor."
    )
    specialization = models.CharField(
        max_length=255,
        help_text="e.g., Cardiologist, Dentist, Pediatrician."
    )
    license_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Professional license or PRC number."
    )
    years_of_experience = models.PositiveIntegerField(
        default=0,
        help_text="Number of years of medical practice."
    )
    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Doctor's consultation fee."
    )
    bio = models.TextField(
        blank=True,
        help_text="Short professional biography or expertise summary."
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Indicates if the doctor is currently accepting appointments."
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        help_text="Average rating (0–5)."
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Display
    def __str__(self):
        full_name = self.user.get_full_name()
        return f"Dr. {full_name or self.user.username} - {self.specialization}"

    class Meta:
        ordering = ['specialization', 'user__last_name']
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"


# -----------------------------
# Doctor Schedule Model
# -----------------------------
class DoctorSchedule(models.Model):
    """Doctor's available time slots per weekday."""

    WEEKDAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='schedules',
        help_text="The doctor this schedule belongs to."
    )
    day_of_week = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor.user.username} - {self.get_day_of_week_display()} ({self.start_time}-{self.end_time})"

    class Meta:
        ordering = ['day_of_week', 'start_time']
        unique_together = ['doctor', 'day_of_week', 'start_time']
        verbose_name = "Doctor Schedule"
        verbose_name_plural = "Doctor Schedules"
