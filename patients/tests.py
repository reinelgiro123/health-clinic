from django.test import TestCase, Client
from django.urls import reverse
from core.models import User
from .models import Patient

class PatientTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='patient1',
            email='patient@example.com',
            password='testpass123',
            role='patient',
            first_name='John',
            last_name='Doe'
        )
        self.patient = Patient.objects.create(
            user=self.user,
            blood_group='O+',
            medical_history='No known allergies'
        )
        self.client.login(username='patient1', password='testpass123')
    
    def test_patient_dashboard_access(self):
        """Test patient can access dashboard"""
        response = self.client.get(reverse('patient_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Patient Dashboard')
    
    def test_patient_profile_view(self):
        """Test patient profile loads"""
        response = self.client.get(reverse('patient_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
    
    def test_patient_model_str(self):
        """Test patient string representation"""
        self.assertEqual(str(self.patient), 'Patient: John Doe')