from rest_framework import serializers, exceptions
from user.models import User
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def _validate_username(self, username, password):
        user = None

        if '@' not in username:
            try:
                temp_user = User.objects.get(username=username)
                username = temp_user.email
            except User.DoesNotExist:
                raise exceptions.ValidationError('Incorrect username or password')

        if username and password:
            user = authenticate(username=username, password=password)
        else:
            raise exceptions.ValidationError('Must include "username" and "password".')

        return user

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = self._validate_username(username, password)
        if user:
            if user.is_active:
                return user
            else:
                raise serializers.ValidationError("User is not active")
        else:
            raise serializers.ValidationError("Incorrect username or password")

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'image']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        username = data.get("username")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User with this username already exists.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user