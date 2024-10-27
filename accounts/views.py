from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import BankAccount,Transaction,Customer
from .serializers import BankAccountSerializer , TransactionSerializer
from datetime import datetime
from rest_framework.permissions import IsAuthenticated



# List all Bank Accounts (GET)
class BankAccountListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if the user has a role and is authorized to set a customer ID
        if hasattr(request.user, 'role') :
            customer_id = request.data.get('customer_id')
            if not customer_id:
                return Response({"error": "Customer ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verify that the customer exists
            try:
                Customer.objects.get(pk=customer_id)
            except Customer.DoesNotExist:
                return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)
            
            request.session['customer_id'] = customer_id
            return Response({"message": "Customer ID has been set."}, status=status.HTTP_200_OK)
        
        return Response({"error": "Permission denied. Only authorized roles can set a customer ID."}, status=status.HTTP_403_FORBIDDEN)

    def get(self, request):
        user = request.user

        if hasattr(user, 'role'):
            customer_id = request.session.get('customer_id')
            if not customer_id:
                return Response({"error": "Customer ID is not set. Please use the POST method to set it first."},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                customer = Customer.objects.get(pk=customer_id)
                accounts = BankAccount.objects.filter(customer=customer)
            except Customer.DoesNotExist:
                return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        else:
            accounts = BankAccount.objects.filter(customer=user)

        serializer = BankAccountSerializer(accounts, many=True)
        return Response(serializer.data)

# Create a Bank Account (POST)
class BankAccountCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not hasattr(request.user, 'role'):
            return Response({"error": "Access denied: User must have a role attribute."}, status=status.HTTP_403_FORBIDDEN)
        # Retrieve customer_id from the request data
        customer_id = request.data.get('customer_id')
        if not customer_id:
            return Response({"error": "Customer ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Verify that the customer exists
        try:
            customer = Customer.objects.get(pk=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        # Add the customer to the request data for the serializer
        data = request.data.copy()
        data['customer'] = customer.id

        serializer = BankAccountSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update, Delete a Bank Account
class BankAccountDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        account = get_object_or_404(BankAccount, pk=pk)
        
        account_number = account.account_number
        customer_name = f"{account.customer.first_name} {account.customer.last_name}"
        
        return Response(
            {"message": f"This is account {account_number} for {customer_name}."},
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        account = get_object_or_404(BankAccount, pk=pk)
        
        serializer = BankAccountSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            
            return Response(
                {"message": "The password has been changed successfully."},
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        account = get_object_or_404(BankAccount, pk=pk)
        
        account_number = account.account_number
        customer_name = f"{account.customer.first_name} {account.customer.last_name}"
        
        account.delete()
        
        return Response(
            {"message": f"The account number {account_number} for customer {customer_name} is deleted."},
            status=status.HTTP_204_NO_CONTENT
        )
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

        if not sender_account.check_transaction_password(transaction_password):
            return Response({"error": "Invalid transaction password."}, status=status.HTTP_401_UNAUTHORIZED)

        if sender_account.balance < int(amount):
            return Response({"error": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

        sender_account.balance -= int(amount)
        receiver_account.balance += int(amount)
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

    def post(self, request):
        # Store the filter conditions from the POST request
        conditions = request.data.get('conditions', {})

        # If no conditions are provided, set to None
        request.session['filter_conditions'] = conditions if conditions else None
        return Response({"message": "Filter conditions have been set."}, status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        sender_account = BankAccount.objects.filter(customer=user)

        queryset = Transaction.objects.filter(sender__in=sender_account).order_by('-timestamp')

        conditions = request.session.get('filter_conditions')

        if conditions:
            tracking_code = conditions.get('tracking_code')
            min_amount = conditions.get('min_amount')
            max_amount = conditions.get('max_amount')
            exact_amount = conditions.get('exact_amount')
            start_date = conditions.get('start_date')
            end_date = conditions.get('end_date')

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

        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)