from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from consultations.serializers import *
from notifications.serializers import *
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class IsProfessionnelSante(permissions.BasePermission):
    """
    Permission personnalisée pour vérifier que l'utilisateur est un professionnel de santé.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour la gestion des patients.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsProfessionnelSante]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['stade_mrc', 'medecin_referent']
    search_fields = ['nom', 'prenom', 'numero_dossier']
    ordering_fields = ['nom', 'date_creation', 'stade_mrc']

    @action(detail=True, methods=['get'])
    def traitements(self, request, pk=None):
        """
        Récupère tous les traitements d'un patient spécifique.
        """
        patient = self.get_object()
        traitements = patient.traitements.all()
        serializer = TraitementEnCoursSerializer(traitements, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Retourne des statistiques sur les patients.
        """
        total_patients = Patient.objects.count()
        stats_par_stade = {}

        for i in range(1, 6):
            count = Patient.objects.filter(stade_mrc=i).count()
            stats_par_stade[f'stade_{i}'] = count

        return Response({
            'total_patients': total_patients,
            'stats_par_stade': stats_par_stade
        })

    @action(detail=True, methods=['get'])
    def dashboard(self, request, pk=None):
        """
        Fournit une vue consolidée pour le tableau de bord d'un patient
        """
        patient = self.get_object()

        # Récupérer les données pertinentes
        traitements_actifs = patient.traitements.filter(est_actif=True)
        dernieres_consultations = patient.consultations.order_by('-date')[:5]
        prochains_rdv = patient.rendez_vous.filter(statut__in=['PLANIFIE', 'CONFIRME']).order_by('date_prevue')
        alertes_actives = patient.alertes.filter(resolue=False).order_by('-priorite', '-date_creation')
        derniers_resultats = patient.resultats_examens.order_by('-date_realisation')[:10]
        evolution_mrc = patient.evolution_mrc.order_by('-date_evaluation')[:5]

        # Sérialiser les données
        data = {
            'patient': PatientSerializer(patient).data,
            'traitements_actifs': TraitementEnCoursSerializer(traitements_actifs, many=True).data,
            'dernieres_consultations': ConsultationSerializer(dernieres_consultations, many=True).data,
            'prochains_rdv': ConsultationPlanifieeSerializer(prochains_rdv, many=True).data,
            'alertes': AlerteCritereSerializer(alertes_actives, many=True).data,
            'derniers_resultats': ResultatExamenSerializer(derniers_resultats, many=True).data,
            'evolution_mrc': SuiviMRCSerializer(evolution_mrc, many=True).data
        }

        return Response(data)



class TraitementViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour la gestion des traitements.
    """
    queryset = TraitementEnCours.objects.all()
    serializer_class = TraitementEnCoursSerializer
    permission_classes = [IsProfessionnelSante]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['patient', 'medicament']
    search_fields = ['medicament', 'patient__nom', 'patient__prenom']

    def perform_create(self, serializer):
        serializer.save(prescripteur=self.request.user)


class ResultatExamenViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour la gestion des résultats d'examens.
    """
    queryset = ResultatExamen.objects.all()
    serializer_class = ResultatExamenSerializer
    permission_classes = [IsProfessionnelSante]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['patient', 'type_examen', 'date_realisation', 'est_anormal']
    search_fields = ['type_examen', 'resultats_texte', 'interpretation']
    ordering_fields = ['date_realisation', 'date_ajout']

    def perform_create(self, serializer):
        resultat = serializer.save(ajoute_par=self.request.user)
        if resultat.est_anormal:
            Notification.objects.create(
                titre=f"Anomalie dans les résultats d'examens de {resultat.patient.nom}",
                message=f"Le résultat {resultat.type_examen} est anormal avec un débit de filtrage urinaire égale à {resultat.dfu} mL / min / 1,73m², une creatinine égale à {resultat.creatinine}, et une protéinurie d'une valeur de {resultat.proteinurie}.{' Cela s\'interprète comme {resultat.interpretation}' if resultat.interpretation else ''}",
                type_notification='ALERTE',
                patient=resultat.patient,
                destinataire=resultat.patient.medecin_referent
            )

    @action(detail=False, methods=['get'])
    def historique_patient(self, request):
        """
        Récupère l'historique des résultats d'examens pour un patient spécifique.
        """
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({"error": "Le paramètre patient_id est requis"}, status=400)

        resultats = ResultatExamen.objects.filter(patient_id=patient_id).order_by('-date_realisation')
        serializer = self.get_serializer(resultats, many=True)

        return Response(serializer.data)

