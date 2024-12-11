from rest_framework import serializers
from .models import BankAccount, Transaction
from Bankusers.models import Customer

class BankAccountSerializer(serializers.ModelSerializer):
    
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)

    class Meta:
        model = BankAccount
        fields = '__all__'
        extra_kwargs = {'account_number': {'required': False}}  # Make account_number optional
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['transaction_password'] = '****'  # Or use a custom masked format
        return representation
    
    
    def validate(self, attrs):
        if 'account_number' in attrs:
            raise serializers.ValidationError({"account_number": "You cannot set the account number manually."})
        return attrs


    def create(self, validated_data):
        return BankAccount.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'customer' in validated_data and instance.customer != validated_data['customer']:
            raise serializers.ValidationError({"customer": "You cannot change the customer after the account is created."})
        
        if 'bank' in validated_data and instance.bank != validated_data['bank']:
            raise serializers.ValidationError({"bank": "You cannot change the bank after the account is created."})
      
        if 'account_number' in validated_data and instance.account_number != validated_data['account_number']:
            raise serializers.ValidationError({"account_number": "You cannot change the account number after creation."})
                
        if 'balance' in validated_data and instance.balance != validated_data['balance']:
            raise serializers.ValidationError({"balance": "You cannot change the account number after creation."})


        return super().update(instance, validated_data)
   
   
    def validate_transaction_password(self, value):
        if len(value) != 4 or not value.isdigit():
            raise serializers.ValidationError("Transaction password must be exactly 4 digits.")
        return value
    

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
      
      
    def validate(self, attrs):
        if 'tracking_code' in attrs:
            raise serializers.ValidationError({"tracking_code": "You cannot set the Tracking code manually."})
        return attrs
