from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def update(self, instance, validated_data):
        if 'email' in validated_data and instance.email != validated_data['email']:
            raise serializers.ValidationError({"email": "You cannot change the email after registration."})

        if 'first_name' in validated_data and instance.first_name != validated_data['first_name']:
            raise serializers.ValidationError({"first_name": "You cannot change the first name after registration."})

        if 'last_name' in validated_data and instance.last_name != validated_data['last_name']:
            raise serializers.ValidationError({"last_name": "You cannot change the last name after registration."})

        return super().update(instance, validated_data)

