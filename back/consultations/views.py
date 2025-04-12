from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import (
    ConsultationSerializer, ConsultationCreateSerializer,
    PrescriptionSerializer, ExamenSerializer, AppointmentSerializer, AppointmentDetailsSerializer
)
from patients.models import TraitementEnCours
from patients.serializers import TraitementEnCoursSerializer
from patients.views import IsProfessionnelSante
from rest_framework.decorators import action
from rest_framework.response import Response
import datetime
from datetime import timezone


class ConsultationViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour la gestion des consultations.
    """
    queryset = Consultation.objects.all()
    serializer_class = ConsultationCreateSerializer
    permission_classes = [IsProfessionnelSante]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'medecin', 'type_consultation']
    search_fields = ['motif', 'diagnostic', 'patient__nom', 'patient__prenom']
    ordering_fields = ['date', 'date_creation']

    # def get_serializer_class(self):
    #     if self.action in ['create', 'update', 'partial_update']:
    #         return ConsultationCreateSerializer
    #     return ConsultationSerializer

    @action(detail=True, methods=['post'])
    def add_prescription(self, request, pk=None):
        consultation = self.get_object()
        serializer = PrescriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(consultation=consultation)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['post'])
    def add_examen(self, request, pk=None):
        consultation = self.get_object()
        serializer = ExamenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(consultation=consultation)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def perform_create(self, serializer):
        if not serializer.validated_data.get('medecin_id'):
            serializer.validated_data['medecin_id'] = self.request.user.id
        serializer.save()

    @action(detail=False, methods=['get'])
    def historique(self, request):
        """
        Récupère l'historique complet des consultations pour un patient donné.
        """
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({"error": "Le paramètre patient_id est requis"}, status=400)

        consultations = Consultation.objects.filter(patient_id=patient_id).order_by('-date')
        serializer = self.get_serializer(consultations, many=True)

        return Response(serializer.data)


class PrescriptionViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour la gestion des prescriptions.
    """
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsProfessionnelSante]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['consultation', 'consultation__patient']
    search_fields = ['medicament', 'consultation__patient__nom']

    @action(detail=True, methods=['post'])
    def creer_traitement(self, request, pk=None):
        """
        Crée un traitement en cours à partir d'une prescription.
        """
        prescription = self.get_object()

        # Vérifier si un traitement existe déjà pour ce médicament
        traitement_existant = TraitementEnCours.objects.filter(
            patient=prescription.consultation.patient,
            medicament=prescription.medicament,
            est_actif=True
        ).first()

        if traitement_existant:
            # Désactiver l'ancien traitement
            traitement_existant.est_actif = False
            traitement_existant.date_fin = datetime.now().date()
            traitement_existant.save()

            # Créer le nouveau traitement lié au précédent
            traitement = TraitementEnCours.objects.create(
                patient=prescription.consultation.patient,
                medicament=prescription.medicament,
                posologie=prescription.posologie,
                date_debut=datetime.now().date(),
                prescripteur=request.user,
                prescription_origine=prescription,
                traitement_precedent=traitement_existant
            )
        else:
            # Créer un nouveau traitement
            traitement = TraitementEnCours.objects.create(
                patient=prescription.consultation.patient,
                medicament=prescription.medicament,
                posologie=prescription.posologie,
                date_debut=datetime.now().date(),
                prescripteur=request.user,
                prescription_origine=prescription
            )

        serializer = TraitementEnCoursSerializer(traitement)
        return Response(serializer.data, status=201)


class ExamenViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour la gestion des examens.
    """
    queryset = Examen.objects.all()
    serializer_class = ExamenSerializer
    permission_classes = [IsProfessionnelSante]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['consultation', 'consultation__patient', 'urgence'] #, 'realise'
    search_fields = ['type_examen', 'consultation__patient__nom']

    @action(detail=True, methods=['post'])
    def marquer_realise(self, request, pk=None):
        examen = self.get_object()
        examen.realise = True
        if 'date_realisation' in request.data:
            examen.date_realisation = request.data['date_realisation']
        if 'resultats' in request.data:
            examen.resultats = request.data['resultats']
        examen.save()
        return Response({'status': 'examen marqué comme réalisé'})


class AppointmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour la gestion des rendez-vous.
    """
    queryset = Appointment.objects.all().order_by('date_prevue')
    serializer_class = AppointmentSerializer
    permission_classes = [IsProfessionnelSante]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'medecin', 'statut'] #, 'type_consultation'
    search_fields = ['motif', 'patient__nom', 'patient__prenom']
    ordering_fields = ['date_prevue']

    def list(self, request, *args, **kwargs):
        date = request.query_params.get('date')
        if date:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            queryset = self.queryset.filter(date_prevue__date=date)
            serializer = AppointmentDetailsSerializer(queryset, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)
    