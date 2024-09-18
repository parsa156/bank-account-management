from rest_framework import viewsets
from .models import BankAccount 
from .serializers import BankAccountSerializer 
class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
