from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import AlerteCritere, Notification, ReglageNotification
from .serializers import (
    AlerteCritereSerializer, NotificationSerializer,
    ReglageNotificationSerializer
)
from patients.views import IsProfessionnelSante
from patients.models import Patient
from consultations.models import Consultation, Examen
from workflows.models import EtapePatient


class AlerteCritereViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour la gestion des critères d'alerte.
    """
    queryset = AlerteCritere.objects.all()
    serializer_class = AlerteCritereSerializer
    permission_classes = [IsProfessionnelSante]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type_alerte', 'actif', 'createur'] # , 'priorite'
    search_fields = ['nom', 'description']

    def perform_create(self, serializer):
        serializer.save(createur=self.request.user)

    @action(detail=True, methods=['post'])
    def evaluer_patients(self, request, pk=None):
        """
        Évalue ce critère d'alerte pour tous les patients et génère des notifications.
        """
        critere = self.get_object()
        patients_ids = request.data.get('patients_ids', None)

        if patients_ids:
            patients = Patient.objects.filter(id__in=patients_ids)
        else:
            patients = Patient.objects.all()

        notifications_count = 0

        # Logique d'évaluation selon le type de critère
        if critere.type_alerte == 'DFU':
            for patient in patients:
                derniere_consultation = Consultation.objects.filter(
                    patient=patient
                ).order_by('-date').first()

                if derniere_consultation and derniere_consultation.dfu_mesure:
                    if derniere_consultation.dfu_mesure < critere.seuil_valeur:
                        # Créer une notification pour le médecin référent
                        if patient.medecin_referent:
                            message = critere.message_template.format(
                                patient=f"{patient.prenom} {patient.nom}",
                                valeur=derniere_consultation.dfu_mesure
                            )

                            Notification.objects.create(
                                titre=f"Alerte DFU - {patient.prenom} {patient.nom}",
                                message=message,
                                type_notification='ALERTE',
                                patient=patient,
                                destinataire=patient.medecin_referent,
                                critere_alerte=critere
                            )
                            notifications_count += 1

        # Autres types de critères...

        return Response({'notifications_crees': notifications_count})


class NotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour la gestion des notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsProfessionnelSante]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type_notification', 'patient', 'critere_alerte'] #, 'lue'
    search_fields = ['titre', 'message', 'patient__nom', 'patient__prenom']

    def get_queryset(self):
        """
        Chaque utilisateur ne voit que ses propres notifications.
        """
        return Notification.objects.filter(destinataire=self.request.user)

    @action(detail=True, methods=['post'])
    def marquer_lue(self, request, pk=None):
        notification = self.get_object()
        notification.lue = True
        notification.date_lecture = timezone.now()
        notification.save()
        return Response({'status': 'notification marquée comme lue'})

    @action(detail=False, methods=['post'])
    def marquer_toutes_lues(self, request):
        self.get_queryset().filter(lue=False).update(
            lue=True,
            date_lecture=timezone.now()
        )
        return Response({'status': 'toutes les notifications marquées comme lues'})

    @action(detail=False, methods=['get'])
    def non_lues(self, request):
        notifications = self.get_queryset().filter(lue=False)
        page = self.paginate_queryset(notifications)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)


class ReglageNotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour la gestion des préférences de notification.
    """
    serializer_class = ReglageNotificationSerializer
    permission_classes = [IsProfessionnelSante]

    def get_queryset(self):
        """
        Chaque utilisateur ne voit que ses propres réglages.
        """
        return ReglageNotification.objects.filter(utilisateur=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Crée ou met à jour les réglages de notification de l'utilisateur.
        """
        # Vérifier si l'utilisateur a déjà des réglages
        try:
            reglage = ReglageNotification.objects.get(utilisateur=request.user)
            serializer = self.get_serializer(reglage, data=request.data)
        except ReglageNotification.DoesNotExist:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)