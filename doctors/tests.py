from django.test import TestCase, Client
from django.urls import reverse
from core.models import User
from .models import Doctor, DoctorSchedule

class DoctorTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='doctor1',
            email='doctor@example.com',
            password='testpass123',
            role='doctor',
            first_name='Jane',
            last_name='Smith'
        )
        self.doctor = Doctor.objects.create(
            user=self.user,
            specialization='Cardiologist',
            license_number='DOC12345',
            years_of_experience=10,
            consultation_fee=150.00
        )
        self.client.login(username='doctor1', password='testpass123')
    
    def test_doctor_dashboard_access(self):
        """Test doctor can access dashboard"""
        response = self.client.get(reverse('doctor_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Doctor Dashboard')
    
    def test_doctor_model_str(self):
        """Test doctor string representation"""
        self.assertEqual(str(self.doctor), 'Dr. Jane Smith - Cardiologist')
    
    def test_doctor_schedule_view(self):
        """Test doctor schedule page loads"""
        response = self.client.get(reverse('doctor_schedule'))
        self.assertEqual(response.status_code, 200)