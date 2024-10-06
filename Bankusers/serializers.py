from rest_framework import serializers
from .models import Employee, Manager, Boss, PendingEmployee
from django.contrib.auth.hashers import make_password

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'

    def validate_code_meli(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Code Meli must be exactly 10 digits and numeric.")
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'first_name' in validated_data and instance.first_name != validated_data['first_name']:
            raise serializers.ValidationError({"first_name": "You cannot change the first name after creation."})

        if 'last_name' in validated_data and instance.last_name != validated_data['last_name']:
            raise serializers.ValidationError({"last_name": "You cannot change the last name after creation."})

        if 'email' in validated_data and instance.email != validated_data['email']:
            raise serializers.ValidationError({"email": "You cannot change the email after creation."})

        if 'code_meli' in validated_data and instance.code_meli != validated_data['code_meli']:
            raise serializers.ValidationError({"code_meli": "You cannot change the national ID (code meli) after creation."})


class EmployeeSerializer(PersonSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class ManagerSerializer(PersonSerializer):
    class Meta:
        model = Manager
        fields = '__all__'

class BossSerializer(PersonSerializer):
    class Meta:
        model = Boss
        fields = '__all__'

class PendingEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingEmployee
        fields = ['first_name', 'last_name', 'code_meli', 'department_id']
