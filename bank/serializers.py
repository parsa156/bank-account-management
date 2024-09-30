from rest_framework import serializers
from .models import Bank

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'name' in validated_data and instance.name != validated_data['name']:
            raise serializers.ValidationError({"name": "You cannot change the name of the bank."})
        
        return super().update(instance, validated_data)
