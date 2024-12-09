# serializers.py
from users.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self,data):
        
        data.pop("role", None)
        
        return data
        
    def create(self, validated_data):
        # Remove the 'role' field from validated_data entirely
        validated_data.pop('role', None)  # Remove the role field if it exists

        # Create the user (without assigning a role)
        user = User.objects.create_user(**validated_data)
        user.save()  # Save the user without the role
        return user