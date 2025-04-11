from django.db import models
from authentication.models import User
from patients.models import Patient, TraitementEnCours
from consultations.models import Consultation, Examen
# from workflows.models import EtapePatient
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta


class AlerteCritere(models.Model):
    """
    Modèle représentant un critère d'alerte personnalisable.
    """
    TYPE_CHOICES = [
        ('DFU', 'DFU en dessous du seuil'),
        ('CREATININE', 'Créatinine au-dessus du seuil'),
        # ('CONSULTATION', 'Délai depuis dernière consultation'),
        ('EXAMEN', 'Résultat d\'examen anormal'),
        # ('ETAPE', 'Étape de workflow en retard'),
        # ('CUSTOM', 'Critère personnalisé'),
        # ('RDV', 'Rendez-vous manqué'),
        # ('TRAITEMENT', 'Fin de traitement proche'),
        # ('AUTRE', 'Autre')
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='alertes')
    nom = models.CharField(max_length=100)
    description = models.TextField()
    type_alerte = models.CharField(max_length=15, choices=TYPE_CHOICES)

    # Seuils pour les différents critères
    seuil_valeur = models.FloatField(null=True, blank=True, help_text="Valeur seuil pour les mesures")
    # seuil_jours = models.IntegerField(null=True, blank=True, help_text="Seuil en jours pour les délais")

    # Niveau de priorité
    # PRIORITE_CHOICES = [
    #     (1, 'Basse'),
    #     (2, 'Moyenne'),
    #     (3, 'Haute'),
    #     (4, 'Urgente'),
    # ]
    # priorite = models.IntegerField(choices=PRIORITE_CHOICES, default=2)

    # Message à afficher
    # message_template = models.TextField(help_text="Template du message d'alerte. Utiliser {patient}, {valeur}, etc.")

    actif = models.BooleanField(default=True)
    createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alertes_criteres')
    date_creation = models.DateTimeField(auto_now_add=True)
    # resolue = models.BooleanField(default=False)
    # date_resolution = models.DateTimeField(null=True, blank=True)

    # Liens optionnels vers les éléments concernés
    # examen_concerne = models.ForeignKey('consultations.Examen', null=True, blank=True, on_delete=models.SET_NULL, related_name='alertes_associees')
    # traitement_concerne = models.ForeignKey(TraitementEnCours, null=True, blank=True, on_delete=models.SET_NULL, related_name='alertes_associees')

    def __str__(self):
        status = "Résolue" if self.resolue else "Active"
        return f"{self.nom} (Priorité: {self.get_priorite_display()})"


class Notification(models.Model):
    """
    Modèle représentant une notification générée par le système.
    """
    TYPE_CHOICES = [
        ('ALERTE', 'Alerte clinique'),
        # ('RAPPEL', 'Rappel de tâche'),
        # ('SYSTEME', 'Notification système'),
        ('RENDEZ_VOUS', 'Rappel de rendez-vous'),
    ]

    titre = models.CharField(max_length=200)
    message = models.TextField()
    type_notification = models.CharField(max_length=12, choices=TYPE_CHOICES)

    # Lien vers un objet concerné (polymorphique)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    # object_id = models.PositiveIntegerField(null=True, blank=True)
    # objet_lie = GenericForeignKey('content_type', 'object_id')

    # Si la notification concerne un patient spécifique
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')

    # Destinataire(s)
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    # Statut
    # lue = models.BooleanField(default=False)
    date_lecture = models.DateTimeField(null=True, blank=True) # La date lecture montre déjà s'il a lu ou pas

    # Si c'est une alerte, référence au critère qui l'a déclenchée
    critere_alerte = models.ForeignKey(AlerteCritere, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications_generees')

    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_expiration = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.titre} - {self.destinataire.username}"
    
    def save(self, force_insert = ..., force_update = ..., using = ..., update_fields = ...):
        # Expire 3 days after creation
        if not self.date_expiration:
            self.date_expiration = self.date_creation + timedelta(days=3)
        super().save(force_insert, force_update, using, update_fields)


class ReglageNotification(models.Model):
    """
    Modèle représentant les préférences de notification d'un utilisateur.
    """
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reglages_notification')

    # Préférences par type
    recevoir_alertes = models.BooleanField(default=True)
    # recevoir_rappels = models.BooleanField(default=True)
    # recevoir_systeme = models.BooleanField(default=True)
    recevoir_rdv = models.BooleanField(default=True)

    # Niveau de priorité minimum pour notification
    # priorite_minimum = models.IntegerField(choices=AlerteCritere.PRIORITE_CHOICES, default=1)

    # Notifications par email
    email_actif = models.BooleanField(default=False)
    # email_priorite_minimum = models.IntegerField(choices=AlerteCritere.PRIORITE_CHOICES, default=3)

    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Réglages de {self.utilisateur.username}"
    