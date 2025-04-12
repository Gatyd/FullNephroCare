from rest_framework import serializers
from .models import *
from patients.serializers import UserSerializer, PatientSerializer


class PrescriptionSerializer(serializers.ModelSerializer):
    consultation = serializers.PrimaryKeyRelatedField(read_only=True)
    patient = serializers.IntegerField(write_only=True)
    class Meta:
        model = Prescription
        fields = ['id', 'consultation', 'patient', 'medicament', 'posologie', 'date_creation', 'duree_traitement', 'instructions', 'est_convertie', 'date_conversion']
        
    def create(self, validated_data):
        patient_id = validated_data.pop('patient', None)
        if patient_id:
            consultation = Consultation.objects.filter(patient_id=patient_id).last()
            if consultation:
                validated_data['consultation'] = consultation
            else:
                raise serializers.ValidationError("Aucune consultation trouvée pour ce patient.")
        else:
            raise serializers.ValidationError("Le patient est requis pour créer un examen.")
        
        return super().create(validated_data)

class ConsultationSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(read_only=True)

    class Meta:
        model = Consultation
        fields = '__all__'


class ExamenSerializer(serializers.ModelSerializer):
    consultation = ConsultationSerializer(read_only=True)
    patient = serializers.IntegerField(write_only=True)
    class Meta:
        model = Examen
        fields = ['id', 'consultation', 'patient', 'type_examen', 'description', 'date_creation', 'date_realisation', 'urgence', 'resultat']

    def create(self, validated_data):
        patient_id = validated_data.pop('patient', None)
        if patient_id:
            consultation = Consultation.objects.filter(patient_id=patient_id).last()
            if consultation:
                validated_data['consultation'] = consultation
            else:
                raise serializers.ValidationError("Aucune consultation trouvée pour ce patient.")
        else:
            raise serializers.ValidationError("Le patient est requis pour créer un examen.")
        
        examen = super().create(validated_data)
        Appointment.objects.create(
            patient=consultation.patient,
            medecin=consultation.medecin,
            date_prevue=examen.date_realisation,
            examen_prealable=examen,
            motif=f"Examen #{examen.id}",
            statut='PLANIFIE'
        )
        return examen
    

class ConsultationCreateSerializer(serializers.ModelSerializer):
    examen = ExamenSerializer(required=False)
    medecin = UserSerializer(read_only=True)

    class Meta:
        model = Consultation
        fields = '__all__'

    def create(self, validated_data):
        validated_data['medecin'] = self.context['request'].user
        examen_data = validated_data.pop('examen', {})

        consultation = Consultation.objects.create(**validated_data)
        if examen_data:
            examen_data['patient'] = consultation.patient.id
            examen = ExamenSerializer(data=examen_data, context=self.context)
            examen.is_valid(raise_exception=True)
            examen = examen.save()
            Appointment.objects.create(
                patient=consultation.patient,
                medecin=consultation.medecin,
                date_prevue=examen.date_realisation,
                examen_prealable=examen,
                motif="Examen de consultation",
                statut='PLANIFIE'
            )

        return consultation
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patient'] = PatientSerializer(instance.patient).data if instance.patient else None
        return representation


class AppointmentSerializer(serializers.ModelSerializer):
    medecin = UserSerializer(read_only=True)
    # patient_details = PatientSerializer(source='patient', read_only=True)
    # examens_prealables = ExamenSerializer(many=True, read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'

    def create(self, validated_data):
        validated_data['medecin'] = self.context['request'].user
        return super().create(validated_data)
    
class AppointmentDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patient'] = PatientSerializer(instance.patient).data if instance.patient else None
        representation['examen_prealable'] = ExamenSerializer(instance.examen_prealable).data if instance.examen_prealable else None
        return representation