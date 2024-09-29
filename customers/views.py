from rest_framework import viewsets
from .models import Customer
from .serializers import CustomerSerializer, CustomerPostSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomerPostSerializer
        return CustomerSerializer
