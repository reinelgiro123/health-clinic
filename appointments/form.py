from django import forms
from django.utils import timezone
import datetime
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Restrict date picker: today or future only
        self.fields['date'].widget.attrs['min'] = timezone.now().date().strftime('%Y-%m-%d')
        # Restrict time picker: between 7:00 AM and 7:00 PM
        self.fields['time'].widget.attrs.update({'min': '07:00', 'max': '19:00'})

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        # ✅ Check for past date
        if date and date < timezone.now().date():
            raise forms.ValidationError("You cannot choose a past date.")

        # ✅ Check time range (7:00 AM – 7:00 PM)
        if time and (time < datetime.time(7, 0) or time > datetime.time(19, 0)):
            raise forms.ValidationError("Please select a time between 7:00 AM and 7:00 PM.")

        return cleaned_data
