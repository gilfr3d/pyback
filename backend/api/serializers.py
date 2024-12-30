import re
from rest_framework import serializers
from .models import CustomUser
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "password", "role", "mobile", "full_name"]
        extra_kwargs = {"password": {"write_only": True, "required": True}}

    def create(self, validated_data):
        # Rely on clean_full_name for validation
        user = CustomUser.objects.create_user(**validated_data)
        return user


class AdminRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'email', 'role', 'mobile', 'full_name']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_mobile(self, value):
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError(
                "Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        return value

    def validate_full_name(self, value):
        # Validate directly without using self.instance
        if not value.strip():
            raise serializers.ValidationError("Full name cannot be blank.")
        return value

    def create(self, validated_data):
        # Ensure full_name is set during registration
        if not validated_data.get('full_name', '').strip():
            raise serializers.ValidationError({"full_name": "This field is required."})

        validated_data['role'] = 'admin'  # Explicitly set role to admin
        user = CustomUser.objects.create_user(**validated_data)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user