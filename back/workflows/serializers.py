from rest_framework import serializers
from .models import Workflow, EtapeWorkflow, PatientWorkflow, EtapePatient
from patients.serializers import UserSerializer, PatientSerializer


class EtapeWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtapeWorkflow
        fields = '__all__'


class WorkflowSerializer(serializers.ModelSerializer):
    etapes = EtapeWorkflowSerializer(many=True, read_only=True)
    createur = UserSerializer(read_only=True)

    class Meta:
        model = Workflow
        fields = '__all__'

    def create(self, validated_data):
        validated_data['createur'] = self.context['request'].user
        return super().create(validated_data)


class WorkflowCreateUpdateSerializer(serializers.ModelSerializer):
    etapes = EtapeWorkflowSerializer(many=True)

    class Meta:
        model = Workflow
        fields = '__all__'

    def create(self, validated_data):
        etapes_data = validated_data.pop('etapes')
        workflow = Workflow.objects.create(**validated_data)

        for etape_data in etapes_data:
            EtapeWorkflow.objects.create(workflow=workflow, **etape_data)

        return workflow

    def update(self, instance, validated_data):
        etapes_data = validated_data.pop('etapes', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if etapes_data is not None:
            # Supprimer les étapes existantes
            instance.etapes.all().delete()

            # Créer les nouvelles étapes
            for etape_data in etapes_data:
                EtapeWorkflow.objects.create(workflow=instance, **etape_data)

            return instance


class EtapePatientSerializer(serializers.ModelSerializer):
    etape_details = EtapeWorkflowSerializer(source='etape', read_only=True)
    responsable = UserSerializer(read_only=True)
    responsable_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = EtapePatient
        fields = '__all__'

    def create(self, validated_data):
        responsable_id = validated_data.pop('responsable_id', None)
        if responsable_id:
            validated_data['responsable_id'] = responsable_id
        return super().create(validated_data)


class PatientWorkflowSerializer(serializers.ModelSerializer):
    patient_details = PatientSerializer(source='patient', read_only=True)
    workflow_details = WorkflowSerializer(source='workflow', read_only=True)
    etapes = EtapePatientSerializer(many=True, read_only=True)

    class Meta:
        model = PatientWorkflow
        fields = '__all__'