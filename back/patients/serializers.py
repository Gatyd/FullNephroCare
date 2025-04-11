from rest_framework import serializers
from .models import *
from authentication.models import User
import random


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class TraitementEnCoursSerializer(serializers.ModelSerializer):
    prescripteur = UserSerializer(read_only=True)
    prescripteur_id = serializers.IntegerField(write_only=True, required=False)
    prescription_origine_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = TraitementEnCours
        fields = '__all__'

class ResultatExamenSerializer(serializers.ModelSerializer):
    ajoute_par = UserSerializer(read_only=True)

    class Meta:
        model = ResultatExamen
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    medecin_referent = UserSerializer(read_only=True)
    numero_dossier = serializers.CharField(required=False)

    class Meta:
        model = Patient
        fields = '__all__'

    def create(self, validated_data):
        validated_data['medecin_referent'] = self.context['request'].user
        if "numero_dossier" not in validated_data or not validated_data["numero_dossier"]:
            validated_data["numero_dossier"] = self.generate_unique_numero_dossier()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        medecin_id = validated_data.pop('medecin_referent_id', None)
        if medecin_id:
            try:
                medecin = User.objects.get(id=medecin_id)
                validated_data['medecin_referent'] = medecin
            except User.DoesNotExist:
                pass
        return super().update(instance, validated_data)

    def generate_unique_numero_dossier(self):
        while True:
            numero = str(random.randint(100000, 999999))  # ou UUID / timestamp
            if not Patient.objects.filter(numero_dossier=numero).exists():
                return numero


class PatientDetailsSerializer(serializers.ModelSerializer):
    traitements = TraitementEnCoursSerializer(many=True, read_only=True)
    examens = ResultatExamenSerializer(many=True, read_only=True)
    medecin_referent = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['traitements', 'examens']