from rest_framework import viewsets
from .models import Bank
from .serializers import BankSerializer, BankPostSerializer

class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BankPostSerializer
        return BankSerializer
