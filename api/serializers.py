from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Furniture

# Existing Furniture Serializer
class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = '__all__'  # Or list specific fields if needed

# New Signup Serializer
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        # Create a new user with the validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# New Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        # Authenticate the user
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            data['user'] = user
            return data
        raise serializers.ValidationError("Invalid credentials")