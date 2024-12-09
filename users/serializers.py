from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from users.models import User
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password','first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        try:
            token = Token.objects.get(key=data['token'])
        except Token.DoesNotExist:
            raise serializers.ValidationError("Invalid token")
        return token
