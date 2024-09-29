from rest_framework import serializers
from .models import BankAccount

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'

class BankAccountPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        request_method = self.context['request'].method
        if request_method == 'POST':
            fields['customer'].read_only = False  
            fields['bank'].read_only = False  
            fields['account_number'].read_only = False  
           
        else:
            fields['customer'].read_only = True  
            fields['bank'].read_only = True  
            fields['account_number'].read_only = True
        return fields
