from rest_framework import serializers
from .models import AlerteCritere, Notification, ReglageNotification
from patients.serializers import UserSerializer, PatientSerializer


class AlerteCritereSerializer(serializers.ModelSerializer):
    createur = UserSerializer(read_only=True)

    class Meta:
        model = AlerteCritere
        fields = '__all__'

    def create(self, validated_data):
        validated_data['createur'] = self.context['request'].user
        return super().create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    patient_details = PatientSerializer(source='patient', read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['date_creation', 'critere_alerte']


class ReglageNotificationSerializer(serializers.ModelSerializer):
    utilisateur = UserSerializer(read_only=True)

    class Meta:
        model = ReglageNotification
        fields = '__all__'
        read_only_fields = ['utilisateur']