from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
from django.core.mail import send_mail
from .models import Appointment
from notifications.models import Notification
from django.conf import settings

class Command(BaseCommand):
    help = "Envoie des rappels de rendez-vous aux patients et notifications aux médecins"

    def handle(self, *args, **kwargs):
        today = now().date()
        dates_cibles = [today + timedelta(days=3), today]  # dans 3 jours ET aujourd'hui

        rdvs = Appointment.objects.filter(
            date_prevue__date__in=dates_cibles,
            statut='PLANIFIE'
        )

        for rdv in rdvs:
            patient = rdv.patient
            medecin = rdv.medecin
            date_str = rdv.date_prevue.strftime("%d/%m/%Y à %H:%M")

            # 1. Envoyer mail au patient
            if patient.email:
                send_mail(
                    subject=f"Rappel : Rendez-vous prévu le {date_str}",
                    message=f"Bonjour {patient.nom},\n\nVous avez un rendez-vous prévu le {date_str}.\nMotif : {rdv.motif}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[patient.email],
                    fail_silently=True,
                )

            # 2. Créer notification pour le médecin
            Notification.objects.create(
                titre="Rappel de rendez-vous",
                message=f"Rappel : Vous avez un rendez-vous avec {patient} le {date_str}.",
                type_notification="RENDEZ_VOUS",
                patient=patient,
                destinataire=medecin
            )

        self.stdout.write(self.style.SUCCESS(f"{rdvs.count()} rappels envoyés."))
