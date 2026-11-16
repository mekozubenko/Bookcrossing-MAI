from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = [
            'login',
            'password',
            'contact_value',
            'contact_type'
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'login', 'contact_value', 'contact_type', 'created_at']
