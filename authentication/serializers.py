from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

class RegisterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def get_fields(self):
        fields = super().get_fields()
        request_method = self.context['request'].method
        if request_method == 'POST':
            fields['email'].read_only = False
        else:
            fields['email'].read_only = True
        return fields

