import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mrc_platform.settings")  # adapte si ton settings s'appelle différemment
django.setup()

from authentication.models import User
from django.contrib.auth.hashers import make_password

def create_admin():
    if not User.objects.filter(email="admin@gmail.com").exists():
        admin = User.objects.create(
            email="admin@gmail.com", 
            password=make_password("12345678"), 
            is_superuser=True, 
            is_staff=True, 
            first_name="Admin", 
            last_name="ADMIN"
        )
        print(f"Creating administrator '{admin.first_name} {admin.last_name}'")
        
    else:
        print(f"Superuser 'admin@gmail.com' already exists. Skipping creation.")

def create_medecin():
    if not User.objects.filter(email='test@gmail.com').exists():
        medecin = User.objects.create(
            email="test@gmail.com",
            password=make_password("12345678"),
            is_staff=True,
            first_name="Medecin",
            last_name="TEST",
        )
        print(f"Creating Médecin '{medecin.first_name} {medecin.last_name}'")
    else:
        print(f"Doctor 'test@gmail.com' already exists. Skipping creation.")

create_admin()
create_medecin()