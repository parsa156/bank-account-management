from rest_framework import serializers
from .models import Customer

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'code_meli', 'phone_number')

    def create(self, validated_data):
        user = Customer.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            code_meli=validated_data['code_meli'],
            password=validated_data['password'],
        )
        return user

    def update(self, instance, validated_data):
        if 'username' in validated_data and instance.username != validated_data['username']:
            raise serializers.ValidationError({"username": "You cannot change the username after registration."})
        
        if 'email' in validated_data and instance.email != validated_data['email']:
            raise serializers.ValidationError({"email": "You cannot change the email after registration."})
        
        if 'code_meli' in validated_data and instance.code_meli != validated_data['code_meli']:
            raise serializers.ValidationError({"code_meli": "You cannot change the code_meli after registration."})
        
        if 'last_name' in validated_data and instance.last_name != validated_data['last_name']:
            raise serializers.ValidationError({"last_name": "You cannot change the last_name after registration."})
        
        if 'first_name' in validated_data and instance.first_name != validated_data['first_name']:
            raise serializers.ValidationError({"first_name": "You cannot change the first_name after registration."})

        return super().update(instance, validated_data)

    def validate_code_meli(self, value):
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError("The national code must be exactly 10 digits and numeric.")
        return value
