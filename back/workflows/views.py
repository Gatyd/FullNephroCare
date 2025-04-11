from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date, timedelta
from .models import Workflow, EtapeWorkflow, PatientWorkflow, EtapePatient
from .serializers import (
    WorkflowSerializer, WorkflowCreateUpdateSerializer,
    EtapeWorkflowSerializer, PatientWorkflowSerializer, EtapePatientSerializer
)
from patients.models import Patient
from patients.serializers import User
from patients.views import IsProfessionnelSante


class WorkflowViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour la gestion des workflows personnalisés.
    """
    queryset = Workflow.objects.all()
    permission_classes = [IsProfessionnelSante]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['stade_mrc', 'actif', 'createur']
    search_fields = ['nom', 'description']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return WorkflowCreateUpdateSerializer
        return WorkflowSerializer

    def perform_create(self, serializer):
        serializer.save(createur=self.request.user)

    @action(detail=True, methods=['post'])
    def appliquer_patient(self, request, pk=None):
        """
        Applique ce workflow à un patient spécifique.
        """
        workflow = self.get_object()
        patient_id = request.data.get('patient_id')
        date_debut = request.data.get('date_debut', date.today())

        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient non trouvé'}, status=404)

        # Créer l'association patient-workflow
        patient_workflow = PatientWorkflow.objects.create(
            patient=patient,
            workflow=workflow,
            date_debut=date_debut
        )

        # Créer les étapes pour ce patient
        etapes = workflow.etapes.all().order_by('ordre')
        current_date = date_debut

        for etape in etapes:
            date_prevue = current_date + timedelta(days=etape.delai_jours)

            EtapePatient.objects.create(
                patient_workflow=patient_workflow,
                etape=etape,
                date_prevue=date_prevue,
                statut='PROGRAMMEE'
            )

            current_date = date_prevue

        return Response(PatientWorkflowSerializer(patient_workflow).data)


class EtapeWorkflowViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour la gestion des étapes de workflow.
    """
    queryset = EtapeWorkflow.objects.all()
    serializer_class = EtapeWorkflowSerializer
    permission_classes = [IsProfessionnelSante]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['workflow', 'type_etape']


class PatientWorkflowViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour la gestion des workflows associés aux patients.
    """
    queryset = PatientWorkflow.objects.all()
    serializer_class = PatientWorkflowSerializer
    permission_classes = [IsProfessionnelSante]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient', 'workflow']

    @action(detail=True, methods=['post'])
    def terminer(self, request, pk=None):
        """
        Marque un workflow patient comme terminé.
        """
        patient_workflow = self.get_object()
        patient_workflow.date_fin = request.data.get('date_fin', date.today())
        patient_workflow.notes = request.data.get('notes', '')
        patient_workflow.save()

        # Optionnel: Marquer toutes les étapes non terminées comme annulées
        etapes_non_terminees = patient_workflow.etapes.exclude(statut='TERMINEE')
        etapes_non_terminees.update(statut='ANNULEE')

        return Response({'status': 'workflow terminé'})


class EtapePatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour la gestion des étapes de workflow pour les patients.
    """
    queryset = EtapePatient.objects.all()
    serializer_class = EtapePatientSerializer
    permission_classes = [IsProfessionnelSante]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['patient_workflow__patient', 'patient_workflow', 'statut', 'responsable']
    search_fields = ['etape__nom', 'commentaire']

    @action(detail=True, methods=['post'])
    def changer_statut(self, request, pk=None):
        """
        Change le statut d'une étape patient.
        """
        etape_patient = self.get_object()
        nouveau_statut = request.data.get('statut')
        if nouveau_statut not in [s[0] for s in EtapePatient.STATUS_CHOICES]:
            return Response({'error': 'Statut invalide'}, status=400)

        etape_patient.statut = nouveau_statut

        if nouveau_statut == 'TERMINEE':
            etape_patient.date_realisation = request.data.get('date_realisation', date.today())

        if 'commentaire' in request.data:
            etape_patient.commentaire = request.data['commentaire']

        if 'responsable_id' in request.data:
            try:
                etape_patient.responsable_id = request.data['responsable_id']
            except User.DoesNotExist:
                pass

        etape_patient.save()
        return Response(EtapePatientSerializer(etape_patient).data)

    @action(detail=False, methods=['get'])
    def prochaines_etapes(self, request):
        """
        Récupère les prochaines étapes programmées.
        """
        jours = int(request.query_params.get('jours', 7))
        date_limite = date.today() + timedelta(days=jours)

        etapes = EtapePatient.objects.filter(
            statut='PROGRAMMEE',
            date_prevue__lte=date_limite
        ).order_by('date_prevue')

        page = self.paginate_queryset(etapes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(etapes, many=True)
        return Response(serializer.data)