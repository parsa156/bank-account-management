from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import BankAccount
from .serializers import BankAccountSerializer 

# List all Bank Accounts (GET)
class BankAccountListView(APIView):
    def get(self, request):
        accounts = BankAccount.objects.all()
        serializer = BankAccountSerializer(accounts, many=True)
        return Response(serializer.data)

# Create a Bank Account (POST)
class BankAccountCreateView(APIView):
    def post(self, request):
        serializer = BankAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update, Delete a Bank Account
class BankAccountDetailView(APIView):
    def get(self, request, pk):
        account = get_object_or_404(BankAccount, pk=pk)
        serializer = BankAccountSerializer(account)
        return Response(serializer.data)

    def put(self, request, pk):
        account = get_object_or_404(BankAccount, pk=pk)
        serializer = BankAccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        account = get_object_or_404(BankAccount, pk=pk)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
