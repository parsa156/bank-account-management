from rest_framework import serializers
from .models import BankAccount

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'customer' in validated_data and instance.customer != validated_data['customer']:
            raise serializers.ValidationError({"customer": "You cannot change the customer after the account is created."})
        
        if 'bank' in validated_data and instance.bank != validated_data['bank']:
            raise serializers.ValidationError({"bank": "You cannot change the bank after the account is created."})
        
        if 'account_number' in validated_data and instance.account_number != validated_data['account_number']:
            raise serializers.ValidationError({"account_number": "You cannot change the account number after creation."})

        return super().update(instance, validated_data)
