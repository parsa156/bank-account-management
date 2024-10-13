from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import BankAccount,Transaction
from .serializers import BankAccountSerializer , TransactionSerializer
from datetime import datetime
from rest_framework.permissions import IsAuthenticated


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

        if not sender_account_number or not receiver_account_number or not amount or not transaction_password:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        sender_account = get_object_or_404(BankAccount, account_number=sender_account_number)
        receiver_account = get_object_or_404(BankAccount, account_number=receiver_account_number)

        if sender_account.customer.transaction_password != transaction_password:
            return Response({"error": "Invalid transaction password."}, status=status.HTTP_401_UNAUTHORIZED)

        if sender_account.balance < float(amount):
            return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

        sender_account.balance -= float(amount)
        receiver_account.balance += float(amount)
        sender_account.save()
        receiver_account.save()

        # Create the transaction
        transaction = Transaction.objects.create(
            sender=sender_account,
            receiver=receiver_account,
            amount=amount
        )

        return Response({
            "message": "Money transferred successfully",
            "tracking_code": transaction.tracking_code,
            "timestamp": transaction.timestamp
        }, status=status.HTTP_200_OK)


class TransactionSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        sender_account = BankAccount.objects.filter(customer=user)
        queryset = Transaction.objects.filter(sender__in=sender_account)

        # Filters
        tracking_code = request.query_params.get('tracking_code')
        min_amount = request.query_params.get('min_amount')
        max_amount = request.query_params.get('max_amount')
        exact_amount = request.query_params.get('exact_amount')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if tracking_code:
            queryset = queryset.filter(tracking_code=tracking_code)
        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)
        if max_amount:
            queryset = queryset.filter(amount__lte=max_amount)
        if exact_amount:
            queryset = queryset.filter(amount=exact_amount)
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                queryset = queryset.filter(timestamp__range=(start_date, end_date))
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # If no filter applied, return all transactions
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)
