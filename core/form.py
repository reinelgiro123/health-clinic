from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from patients.models import Patient
from doctors.models import Doctor

# -----------------------------
# User Registration Form
# -----------------------------
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=15, required=False)
    date_of_birth = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}), 
        required=False
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'phone', 'date_of_birth', 'address', 'password1', 'password2'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

# -----------------------------
# Patient Registration Form
# -----------------------------
class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['blood_group', 'medical_history', 'emergency_contact_name', 'emergency_contact_phone']
        widgets = {
            'medical_history': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'blood_group': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

# -----------------------------
# Doctor Registration Form
# -----------------------------
class DoctorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization', 'license_number', 'years_of_experience', 'consultation_fee', 'bio']
        widgets = {
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }


# =========================================================================
# PROFILE UPDATE FORMS (New additions for edit_profile view)
# =========================================================================

class UserUpdateForm(forms.ModelForm):
    """Form to allow users to update core fields on the User model."""
    
    # Exclude username and password for security/simplicity.
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            # Note: email, first_name, last_name, phone will inherit 'form-control' via __init__
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Apply form-control class to all remaining fields
            if 'class' not in field.widget.attrs:
                field.widget.attrs.update({'class': 'form-control'})
            
        # Ensure email cannot be blank when updating and add validation
        self.fields['email'].required = True

    def clean_email(self):
        # Check if email is unique (unless it belongs to the current user instance)
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email address is already in use by another account.")
        return email


class PatientUpdateForm(forms.ModelForm):
    """Form for Patient-specific profile fields."""
    class Meta:
        model = Patient
        fields = ['blood_group', 'medical_history', 'emergency_contact_name', 'emergency_contact_phone']
        widgets = {
            'medical_history': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'blood_group': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DoctorUpdateForm(forms.ModelForm):
    """Form for Doctor-specific profile fields."""
    class Meta:
        model = Doctor
        fields = ['specialization', 'license_number', 'years_of_experience', 'consultation_fee', 'bio']
        widgets = {
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
