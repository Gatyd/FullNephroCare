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


class ExamenSerializer(serializers.ModelSerializer):
    consultation = serializers.PrimaryKeyRelatedField(read_only=True)
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
        
        return super().create(validated_data)

class ConsultationSerializer(serializers.ModelSerializer):
    medecin = UserSerializer(read_only=True)
    medecin_id = serializers.IntegerField(write_only=True)
    patient_details = PatientSerializer(source='patient', read_only=True)
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    examens = ExamenSerializer(many=True, read_only=True)

    class Meta:
        model = Consultation
        fields = '__all__'

    def create(self, validated_data):
        medecin_id = validated_data.pop('medecin_id')
        validated_data['medecin_id'] = medecin_id
        return super().create(validated_data)


class ConsultationCreateSerializer(serializers.ModelSerializer):
    prescriptions = PrescriptionSerializer(many=True, required=False)
    examens = ExamenSerializer(many=True, required=False)

    class Meta:
        model = Consultation
        fields = '__all__'

    def create(self, validated_data):
        prescriptions_data = validated_data.pop('prescriptions', [])
        examens_data = validated_data.pop('examens', [])

        consultation = Consultation.objects.create(**validated_data)

        for prescription_data in prescriptions_data:
            Prescription.objects.create(consultation=consultation, **prescription_data)

        for examen_data in examens_data:
            Examen.objects.create(consultation=consultation, **examen_data)

        return consultation


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
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patient'] = PatientSerializer(instance.patient).data if instance.patient else None
        return representation
    
class AppointmentDetailsSerializer(serializers.ModelSerializer):
    medecin = UserSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    examens_prealables = ExamenSerializer(many=True, read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'