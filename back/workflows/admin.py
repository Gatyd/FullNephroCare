from django.contrib import admin
from .models import Workflow, EtapeWorkflow, PatientWorkflow, EtapePatient

class EtapeWorkflowInline(admin.TabularInline):
    model = EtapeWorkflow
    extra = 1
    ordering = ('ordre',)

@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ('nom', 'stade_mrc', 'createur', 'actif', 'date_creation')
    list_filter = ('stade_mrc', 'actif', 'createur')
    search_fields = ('nom', 'description')
    inlines = [EtapeWorkflowInline]

class EtapePatientInline(admin.TabularInline):
    model = EtapePatient
    extra = 1
    ordering = ('date_prevue',)

@admin.register(PatientWorkflow)
class PatientWorkflowAdmin(admin.ModelAdmin):
    list_display = ('patient', 'workflow', 'date_debut', 'date_fin')
    list_filter = ('workflow', 'date_debut')
    search_fields = ('patient__nom', 'patient__prenom', 'workflow__nom')
    inlines = [EtapePatientInline]

@admin.register(EtapePatient)
class EtapePatientAdmin(admin.ModelAdmin):
    list_display = ('etape', 'patient_workflow', 'date_prevue', 'statut', 'responsable')
    list_filter = ('statut', 'responsable')
    search_fields = ('etape__nom', 'patient_workflow__patient__nom')
    date_hierarchy = 'date_prevue'