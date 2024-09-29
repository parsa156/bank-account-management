from rest_framework import serializers
from .models import Bank

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

class BankPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        request_method = self.context['request'].method
        if request_method == 'POST':
            fields['name'].read_only = False  # Make 'name' editable during POST
        else:
            fields['name'].read_only = True
        return fields
