# serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self,data):
        
        data.pop("role", None)
        
        return data
        
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
