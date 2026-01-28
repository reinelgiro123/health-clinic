from django.test import TestCase, Client
from django.urls import reverse
from core.models import User
from patients.models import Patient
from doctors.models import Doctor
from .models import Appointment
from datetime import date, time

class AppointmentTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create patient
        self.patient_user = User.objects.create_user(
            username='patient1',
            email='patient@example.com',
            password='testpass123',
            role='patient'
        )
        self.patient = Patient.objects.create(user=self.patient_user)
        
        # Create doctor
        self.doctor_user = User.objects.create_user(
            username='doctor1',
            email='doctor@example.com',
            password='testpass123',
            role='doctor'
        )
        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            specialization='General Physician',
            license_number='DOC123'
        )
        
        # Create appointment
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=date(2025, 12, 1),
            appointment_time=time(10, 0),
            reason='Regular checkup',
            status='pending'
        )
        
        self.client.login(username='patient1', password='testpass123')
    
    def test_appointment_creation(self):
        """Test appointment is created correctly"""
        self.assertEqual(self.appointment.status, 'pending')
        self.assertEqual(self.appointment.patient, self.patient)
        self.assertEqual(self.appointment.doctor, self.doctor)
    
    def test_cancel_appointment(self):
        """Test patient can cancel appointment"""
        response = self.client.get(
            reverse('cancel_appointment', args=[self.appointment.id])
        )
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'cancelled')
    
    def test_appointment_model_str(self):
        """Test appointment string representation"""
        expected = f"patient1 → Dr. doctor1 on 2025-12-01"
        self.assertEqual(str(self.appointment), expected)