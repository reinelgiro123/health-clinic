from django.db import models
from django.conf import settings
# Assuming 'User' is needed elsewhere, otherwise using settings.AUTH_USER_MODEL is best practice
from core.models import User 


class Patient(models.Model):
    """Patient profile extending the custom User model."""

    # -----------------------------
    # Relationship
    # -----------------------------
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_profile',
        help_text="Linked user account for the patient."
        # The incorrect line defining the field inside itself has been removed.
    )

    # -----------------------------
    # Basic Info
    # -----------------------------
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Primary contact number of the patient."
    )
    blood_group = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        help_text="Blood group of the patient, e.g., O+, A-."
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="Date of birth of the patient."
    )

    # -----------------------------
    # Health & Insurance
    # -----------------------------
    medical_history = models.TextField(
        blank=True,
        default='',
        help_text="Previous conditions, allergies, medications, etc."
    )
    insurance_number = models.CharField(
        max_length=50,
        blank=True,
        default='',
        help_text="Insurance or health plan number."
    )

    # -----------------------------
    # Emergency Contact
    # -----------------------------
    emergency_contact_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        help_text="Name of emergency contact person."
    )
    emergency_contact_phone = models.CharField(
        max_length=15,
        blank=True,
        default='',
        help_text="Phone number of emergency contact person."
    )

    # -----------------------------
    # Status & Metadata
    # -----------------------------
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates if the patient is currently active."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -----------------------------
    # Display
    # -----------------------------
    def __str__(self):
        """Return a readable string for the patient."""
        full_name = self.user.get_full_name()
        return f"Patient: {full_name or self.user.username}"

    class Meta:
        ordering = ['-user__username']
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
