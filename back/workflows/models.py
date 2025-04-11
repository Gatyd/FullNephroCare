from django.db import models
from authentication.models import User
from patients.models import Patient


class Workflow(models.Model):
    """
    Modèle représentant un workflow personnalisé pour le suivi des patients.
    """
    nom = models.CharField(max_length=100)
    description = models.TextField()
    stade_mrc = models.IntegerField(choices=[(i, f"Stade {i}") for i in range(1, 6)], blank=True, null=True)
    createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workflows_crees')
    actif = models.BooleanField(default=True)

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} (Stade {self.stade_mrc if self.stade_mrc else 'Tous'})"

    class Meta:
        verbose_name = "Workflow"
        verbose_name_plural = "Workflows"


class EtapeWorkflow(models.Model):
    """
    Modèle représentant une étape dans un workflow.
    """
    TYPE_CHOICES = [
        ('EXAMEN', 'Examen médical'),
        ('CONSULTATION', 'Consultation'),
        ('TRAITEMENT', 'Ajustement traitement'),
        ('EDUCATION', 'Éducation patient'),
        ('AUTRE', 'Autre action'),
    ]

    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='etapes')
    nom = models.CharField(max_length=100)
    description = models.TextField()
    type_etape = models.CharField(max_length=15, choices=TYPE_CHOICES)

    # Délais et périodicité
    delai_jours = models.IntegerField(help_text="Délai en jours après l'étape précédente ou le début du workflow")
    periodique = models.BooleanField(default=False)
    periodicite_jours = models.IntegerField(null=True, blank=True,
                                            help_text="Pour les actions périodiques, intervalle en jours")

    # Ordre de l'étape dans le workflow
    ordre = models.IntegerField()

    class Meta:
        ordering = ['workflow', 'ordre']

    def __str__(self):
        return f"{self.nom} ({self.workflow.nom})"


class PatientWorkflow(models.Model):
    """
    Modèle représentant l'association entre un patient et un workflow.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='workflows')
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='patients')
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.workflow}"


class EtapePatient(models.Model):
    """
    Modèle représentant une étape de workflow pour un patient spécifique.
    """
    STATUS_CHOICES = [
        ('PROGRAMMEE', 'Programmée'),
        ('EN_COURS', 'En cours'),
        ('TERMINEE', 'Terminée'),
        ('ANNULEE', 'Annulée'),
    ]

    patient_workflow = models.ForeignKey(PatientWorkflow, on_delete=models.CASCADE, related_name='etapes')
    etape = models.ForeignKey(EtapeWorkflow, on_delete=models.CASCADE, related_name='realisations')
    date_prevue = models.DateField()
    statut = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PROGRAMMEE')

    date_realisation = models.DateField(null=True, blank=True)
    commentaire = models.TextField(blank=True)

    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='etapes_assignees')

    class Meta:
        ordering = ['date_prevue']

    def __str__(self):
        return f"{self.etape.nom} - {self.patient_workflow.patient} ({self.get_statut_display()})"