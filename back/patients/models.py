from django.db import models
from authentication.models import User


class Patient(models.Model):
    """
    Modèle représentant un patient atteint de Maladie Rénale Chronique.
    """
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre'),
    ]

    numero_dossier = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)

    # Données médicales
    stade_mrc = models.IntegerField(choices=[(i, f"Stade {i}") for i in range(1, 6)], blank=True, null=True)
    dfu = models.FloatField(blank=True, null=True, verbose_name="Débit de Filtration Urinaire")
    antecedents_medicaux = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)

    # Informations administratives
    medecin_referent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='patients')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} (Dossier: {self.numero_dossier})"

    class Meta:
        ordering = ['nom', 'prenom']
        verbose_name = "Patient"
        verbose_name_plural = "Patients"


class TraitementEnCours(models.Model):
    """
    Modèle représentant les traitements en cours pour un patient.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='traitements')
    medicament = models.CharField(max_length=200)
    posologie = models.CharField(max_length=200)
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    prescripteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    commentaire = models.TextField(blank=True, null=True)

    # Nouveau champ pour lier à la prescription d'origine
    prescription_origine = models.ForeignKey('consultations.Prescription', on_delete=models.SET_NULL, null=True, blank=True, related_name='traitements_resultants')

    # Nouveau champ pour suivre les modifications
    est_actif = models.BooleanField(default=True)
    date_modification = models.DateTimeField(auto_now=True)
    traitement_precedent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='traitement_suivant')

    def __str__(self):
        return f"{self.medicament} - {self.patient}"


class ResultatExamen(models.Model):
    """
    Modèle pour stocker les résultats d'examens pour un patient, indépendamment des consultations.
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='resultats_examens')
    examen_prescrit = models.ForeignKey('consultations.Examen', on_delete=models.SET_NULL, null=True, blank=True, related_name='resultats_examen_prescrit+')

    type_examen = models.CharField(max_length=200)
    date_realisation = models.DateField()
    laboratoire = models.CharField(max_length=200, blank=True, null=True)

    # Résultats spécifiques (on pourrait créer des sous-classes pour différents types d'examens)
    resultats_texte = models.TextField(blank=True, null=True)
    fichier_resultats = models.FileField(upload_to='resultats_examens/', null=True, blank=True)

    # Valeurs courantes pour MRC
    creatinine = models.FloatField(null=True, blank=True)
    dfu = models.FloatField(null=True, blank=True, verbose_name="Débit de Filtration Urinaire")
    proteinurie = models.FloatField(null=True, blank=True)
    # Autres champs pertinents pour les examens de MRC...

    interpretation = models.TextField(blank=True, null=True, help_text="Interprétation médicale des résultats")
    est_anormal = models.BooleanField(default=False)

    date_ajout = models.DateTimeField(auto_now_add=True)
    ajoute_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-date_realisation']

    def __str__(self):
        return f"{self.type_examen} - {self.patient} ({self.date_realisation})"
