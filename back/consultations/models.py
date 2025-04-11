from django.db import models
from authentication.models import User
from patients.models import Patient, ResultatExamen
from django.core.validators import MaxValueValidator, MinValueValidator

class Consultation(models.Model):
    """
    Modèle représentant une consultation médicale.
    """
    TYPE_CHOICES = [
        ('INITIALE', 'Consultation initiale'),
        ('SUIVI', 'Consultation de suivi'),
        ('URGENCE', 'Consultation d\'urgence'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    medecin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultations_effectuees')
    date = models.DateTimeField()
    type_consultation = models.CharField(max_length=10, choices=TYPE_CHOICES)

    # motif = models.TextField()
    symptomes = models.TextField(blank=True)
    diagnostic = models.TextField(blank=True)
    # recommandations = models.TextField(blank=True)

    def __str__(self):
        return f"Consultation du {self.date.strftime('%d/%m/%Y')} - {self.patient}"

    class Meta:
        ordering = ['-date']
        verbose_name = "Consultation"
        verbose_name_plural = "Consultations"


class Prescription(models.Model):
    """
    Modèle représentant une prescription médicale.
    """
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='prescriptions')
    medicament = models.CharField(max_length=200)
    posologie = models.CharField(max_length=200)
    duree_traitement = models.PositiveBigIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3650)]) # en jours
    instructions = models.TextField(blank=True, null=True)

    # Nouveaux champs pour le suivi
    est_convertie = models.BooleanField(default=False)
    date_conversion = models.DateTimeField(null=True, blank=True)
    # convertie_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='prescriptions_converties', blank=True)
    
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicament} - {self.consultation.patient}"


class Examen(models.Model):
    """
    Modèle représentant un examen médical prescrit.
    """
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='examens')
    type_examen = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date_realisation = models.DateField() # date_prescrite => date_realisation ça revient à la date où l'examen doit être réalisé
    urgence = models.BooleanField(default=False)

    # Suivi de l'examen
    # realise = models.BooleanField(default=False) resultat != null montre si l'examen a été réalisé ou pas

    # Pour faciliter la navigation vers les résultats:
    # resultats = models.ManyToManyField('patients.ResultatExamen', blank=True, related_name='examens_consultation_associes')
    resultat = models.OneToOneField(ResultatExamen, on_delete=models.CASCADE, blank=True, null=True, related_name='examen')

    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Réalisé" if self.realise else "En attente"
        return f"{self.type_examen} - {self.consultation.patient} ({status})"


class Appointment(models.Model):
    """
    Modèle pour les rendez-vous à venir
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rendez_vous')
    medecin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultations_planifiees')
    date_prevue = models.DateTimeField()
    # type_consultation = models.CharField(max_length=10, choices=Consultation.TYPE_CHOICES)
    motif = models.TextField()
    notes_preparation = models.TextField(blank=True, null=True)
    examen_prealable = models.ForeignKey(Examen, blank=True, null=True, on_delete=models.CASCADE, related_name='appointments')

    # Suivi
    statut = models.CharField(max_length=20, choices=[
        ('PLANIFIE', 'Planifié'),
        # ('CONFIRME', 'Confirmé'),
        ('ANNULE', 'Annulé'),
        ('COMPLETE', 'Complété')
    ], default='PLANIFIE')
    # consultation_realisee = models.OneToOneField(Consultation, null=True, blank=True, on_delete=models.SET_NULL, related_name='planification')

    def __str__(self):
        return f"RDV {self.patient} - {self.date_prevue.strftime('%d/%m/%Y %H:%M')}"
