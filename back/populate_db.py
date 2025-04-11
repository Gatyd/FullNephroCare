from faker import Faker
import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mrc_platform.settings')
django.setup()

from authentication.models import User
from patients.models import Patient
fake = Faker()

def generate_medecins(num=10):
    for _ in range(num):
        User.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            password=make_password('12345678'),
            is_active=True,
            is_staff=True,
        )
        print(f"Medecin {fake.first_name()} {fake.last_name()} créé.")

def generate_patients(num=40):
    for _ in range(num):
        Patient.objects.create(
            numero_dossier=fake.unique.random_int(min=100000, max=999999),
            nom=fake.last_name(),
            prenom=fake.first_name(),
            date_naissance=fake.date_of_birth(minimum_age=18, maximum_age=90),
            sexe=fake.random_element(elements=('M', 'F')),
            adresse=fake.address(),
            telephone=fake.phone_number(),
            email=fake.email(),
            stade_mrc=fake.random_int(min=1, max=5),
            dfu=fake.random_number(digits=3, fix_len=True) / 10,
            antecedents_medicaux=fake.text(max_nb_chars=200),
            allergies=fake.text(max_nb_chars=100),
            medecin_referent=User.objects.order_by('?').first(),  # Assign a random doctor
        )
        print(f"Patient {fake.first_name()} {fake.last_name()} créé.")

generate_medecins(10)  # Generate 10 doctors
generate_patients(40)  # Generate 40 patients