from django.contrib import admin
from .models import Patient, TraitementEnCours, ResultatExamen

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'numero_dossier', 'date_naissance', 'stade_mrc', 'medecin_referent')
    list_filter = ('stade_mrc', 'sexe')
    search_fields = ('nom', 'prenom', 'numero_dossier')
    raw_id_fields = ('medecin_referent',)
    ordering = ('nom', 'prenom')

@admin.register(TraitementEnCours)
class TraitementEnCoursAdmin(admin.ModelAdmin):
    list_display = ('medicament', 'patient', 'posologie', 'date_debut', 'date_fin', 'est_actif')
    list_filter = ('est_actif', 'date_debut')
    search_fields = ('medicament', 'patient__nom')
    raw_id_fields = ('patient', 'prescripteur', 'prescription_origine', 'traitement_precedent')

@admin.register(ResultatExamen)
class ResultatExamenAdmin(admin.ModelAdmin):
    list_display = ('type_examen', 'patient', 'date_realisation', 'est_anormal')
    list_filter = ('type_examen', 'est_anormal')
    search_fields = ('type_examen', 'patient__nom', 'resultats_texte')
    date_hierarchy = 'date_realisation'
    raw_id_fields = ('patient', 'examen_prescrit', 'ajoute_par')

