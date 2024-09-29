from rest_framework import viewsets
from .models import BankAccount
from .serializers import BankAccountSerializer, BankAccountPostSerializer

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BankAccountPostSerializer
        return BankAccountSerializer
