from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Bank
from .serializers import BankSerializer 

# List all Banks (GET)
class BankListView(APIView):
    def get(self, request):
        banks = Bank.objects.all()
        serializer = BankSerializer(banks, many=True)
        return Response(serializer.data)

# Create a Bank (POST)
class BankCreateView(APIView):
    def post(self, request):
        serializer = BankSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update, Delete a Bank
class BankDetailView(APIView):
    def get(self, request, pk):
        bank = get_object_or_404(Bank, pk=pk)
        serializer = BankSerializer(bank)
        return Response(serializer.data)

    def put(self, request, pk):
        bank = get_object_or_404(Bank, pk=pk)
        serializer = BankSerializer(bank, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        bank = get_object_or_404(Bank, pk=pk)
        bank.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
