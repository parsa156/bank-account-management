
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Bank
from .serializers import BankSerializer

class BankViewSet(viewsets.ModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated]
