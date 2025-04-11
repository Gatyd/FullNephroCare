from django.contrib import admin
from .models import Consultation, Prescription, Examen, Appointment

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medecin', 'date', 'type_consultation')
    list_filter = ('type_consultation', 'date')
    search_fields = ('patient__nom', 'patient__prenom', 'motif', 'diagnostic')
    date_hierarchy = 'date'
    raw_id_fields = ('patient', 'medecin')
    ordering = ('-date',)

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medicament', 'consultation', 'posologie', 'duree_traitement')#, 'est_convertie_en_traitement'
    #list_filter = ('est_convertie_en_traitement',)
    search_fields = ('medicament', 'consultation__patient__nom')
    raw_id_fields = ('consultation',)#, 'convertie_par'

@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
    list_display = ('type_examen', 'consultation', 'urgence') #, 'realise', 'date_prescrite'
    list_filter = ('urgence', 'type_examen') #, 'realise'
    search_fields = ('type_examen', 'consultation__patient__nom')
    raw_id_fields = ('consultation',)

@admin.register(Appointment)
class ConsultationPlanifieeAdmin(admin.ModelAdmin):
    list_display = ('patient', 'medecin', 'date_prevue', 'statut') #, 'type_consultation'
    list_filter = ('statut',) #, 'type_consultation'
    search_fields = ('patient__nom', 'patient__prenom', 'motif')
    date_hierarchy = 'date_prevue'
    raw_id_fields = ('patient', 'medecin') # , 'consultation_realisee'