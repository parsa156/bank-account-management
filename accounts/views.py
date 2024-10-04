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
#Transfer Money
class TransferMoneyView(APIView):
    def post(self, request):
        sender_account_number = request.data.get('sender_account_number')
        receiver_account_number = request.data.get('receiver_account_number')
        amount = request.data.get('amount')
        transaction_password = request.data.get('transaction_password')

        # Validate inputs
        if not sender_account_number or not receiver_account_number or not amount or not transaction_password:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        sender_account = get_object_or_404(BankAccount, account_number=sender_account_number)
        receiver_account = get_object_or_404(BankAccount, account_number=receiver_account_number)

        # Check transaction password
        if sender_account.customer.transaction_password != transaction_password:
            return Response({"error": "Invalid transaction password."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check sufficient balance
        if sender_account.balance < float(amount):
            return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

        # Transfer money
        sender_account.balance -= float(amount)
        receiver_account.balance += float(amount)
        sender_account.save()
        receiver_account.save()

        return Response({"message": "Money transferred successfully"}, status=status.HTTP_200_OK)
