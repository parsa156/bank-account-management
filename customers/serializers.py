from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        request_method = self.context['request'].method
        if request_method == 'POST':
            fields['email'].read_only = False  
            fields['first_name'].read_only = False  
            fields['last_name'].read_only = False  

        else:
            fields['email'].read_only = True
            fields['first_name'].read_only = True  
            fields['last_name'].read_only = True  

        return fields
