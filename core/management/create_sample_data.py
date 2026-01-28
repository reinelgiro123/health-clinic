from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from patients.models import Patient
from doctors.models import Doctor, DoctorSchedule
from appointments.models import Appointment
from datetime import date, time, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')
        
        # Create patients
        patient_user1 = User.objects.create_user(
            username='john_doe',
            email='john@example.com',
            password='patient123',
            role='patient',
            first_name='John',
            last_name='Doe',
            phone='555-0101'
        )
        patient1 = Patient.objects.create(
            user=patient_user1,
            blood_group='O+',
            medical_history='No known allergies'
        )
        
        patient_user2 = User.objects.create_user(
            username='jane_smith',
            email='jane@example.com',
            password='patient123',
            role='patient',
            first_name='Jane',
            last_name='Smith',
            phone='555-0102'
        )
        patient2 = Patient.objects.create(
            user=patient_user2,
            blood_group='A+',
            medical_history='Asthma'
        )
        
        # Create doctors
        doctor_user1 = User.objects.create_user(
            username='dr_wilson',
            email='wilson@example.com',
            password='doctor123',
            role='doctor',
            first_name='James',
            last_name='Wilson',
            phone='555-0201'
        )
        doctor1 = Doctor.objects.create(
            user=doctor_user1,
            specialization='Cardiologist',
            license_number='DOC001',
            years_of_experience=15,
            consultation_fee=200.00,
            bio='Experienced cardiologist with 15 years of practice'
        )
        
        doctor_user2 = User.objects.create_user(
            username='dr_chase',
            email='chase@example.com',
            password='doctor123',
            role='doctor',
            first_name='Robert',
            last_name='Chase',
            phone='555-0202'
        )
        doctor2 = Doctor.objects.create(
            user=doctor_user2,
            specialization='General Physician',
            license_number='DOC002',
            years_of_experience=10,
            consultation_fee=150.00,
            bio='Family medicine specialist'
        )
        
        # Create doctor schedules
        for day in range(5):  # Monday to Friday
            DoctorSchedule.objects.create(
                doctor=doctor1,
                day_of_week=day,
                start_time=time(9, 0),
                end_time=time(17, 0)
            )
            DoctorSchedule.objects.create(
                doctor=doctor2,
                day_of_week=day,
                start_time=time(8, 0),
                end_time=time(16, 0)
            )
        
        # Create appointments
        today = date.today()
        Appointment.objects.create(
            patient=patient1,
            doctor=doctor1,
            appointment_date=today + timedelta(days=1),
            appointment_time=time(10, 0),
            reason='Regular checkup',
            status='confirmed'
        )
        
        Appointment.objects.create(
            patient=patient1,
            doctor=doctor2,
            appointment_date=today + timedelta(days=3),
            appointment_time=time(14, 0),
            reason='Follow-up consultation',
            status='pending'
        )
        
        Appointment.objects.create(
            patient=patient2,
            doctor=doctor1,
            appointment_date=today + timedelta(days=2),
            appointment_time=time(11, 0),
            reason='Cardiac evaluation',
            status='confirmed'
        )
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('Patient credentials:')
        self.stdout.write('  Username: john_doe | Password: patient123')
        self.stdout.write('  Username: jane_smith | Password: patient123')
        self.stdout.write('Doctor credentials:')
        self.stdout.write('  Username: dr_wilson | Password: doctor123')
        self.stdout.write('  Username: dr_chase | Password: doctor123')