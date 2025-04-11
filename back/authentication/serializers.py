from .models import User
from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError({
                "Connexion impossible": "Identifiants invalides"
            })
        data['user'] = user
        return data

class UserSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only = True, required=False)
    class Meta:
        model = User
        fields = ['id','email','first_name','last_name','is_staff','is_superuser','current_password']

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if not user.is_superuser:
            current_password = validated_data.pop('current_password', None)
            if current_password:
                if not instance.check_password(current_password):
                    raise serializers.ValidationError({"Erreur": "Mot de passe actuel incorrect."})
            if 'password' in validated_data and not current_password:
                raise serializers.ValidationError({"Erreur": "Le mot de passe actuel est requis pour changer le mot de passe."})
            if 'password' in validated_data:
                instance.set_password(validated_data.pop('password'))
        instance = super().update(instance, validated_data)
        instance.save()
        return instance
    