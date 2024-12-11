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
        user = request.user
        role = user.role
        
        # Check if the user is a Customer and get the related customer instance
        if role == 'Customer':
            customer = user.customer  # Ensure `user` has a related `Customer` instance
        else:
            # For other roles, retrieve customer_id from request data
            customer_id = request.data.get('customer_id')
            if not customer_id:
                return Response({"error": "Customer ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verify that the customer exists
            try:
                customer = Customer.objects.get(pk=customer_id)
            except Customer.DoesNotExist:
                return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        # Fetch accounts for the identified customer
        accounts = BankAccount.objects.filter(customer=customer)
        serializer = BankAccountSerializer(accounts, many=True)
        
        return Response({
            "message": "Customer ID is valid.",
            "accounts": serializer.data
        }, status=status.HTTP_200_OK)
        
# Create a Bank Account (POST)
class BankAccountCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        role = user.role
        if role == 'Customer':
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        
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
        user = request.user
        role = user.role
        
        # Deny access if the user role is Customer
        if role == 'Customer':
            return Response(
                {"error": "Permission denied. Customers are not allowed to delete accounts."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Proceed with deletion for authorized roles
        account = get_object_or_404(BankAccount, pk=pk)
        account_number = account.account_number
        customer_name = f"{account.customer.first_name} {account.customer.last_name}"
        
        account.delete()
        
        return Response(
            {"message": f"The account number {account_number} for customer {customer_name} is deleted."},
            status=status.HTTP_200_OK
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


from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class TransactionSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        role = user.role
        
        # Get customer instance based on role
        if role == 'Customer':
            customer = user.customer  # Automatically get `Customer` from `user`
            sender_accounts = BankAccount.objects.filter(customer=customer)  # Get all accounts for the customer
        else:
            # For non-Customer roles, retrieve customer_id from the request
            customer_id = request.data.get('customer_id')
            if not customer_id:
                return Response({"error": "Customer ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verify that the customer exists
            customer = get_object_or_404(Customer, pk=customer_id)
            sender_accounts = BankAccount.objects.filter(customer=customer)  # Get accounts for the specified customer
        
        # Start with transactions where sender account belongs to the customer
        queryset = Transaction.objects.filter(sender__in=sender_accounts).order_by('-timestamp')
        
        # Store messages for conditions
        messages = []

        # Apply filtering conditions from the request
        conditions = request.data.get('conditions', {})

        if conditions:
            tracking_code = conditions.get('tracking_code')
            min_amount = conditions.get('min_amount')
            max_amount = conditions.get('max_amount')
            exact_amount = conditions.get('exact_amount')
            start_date = conditions.get('start_date')
            end_date = conditions.get('end_date')
            receiver_account = conditions.get('receiver_account')
            sender_account_id = conditions.get('sender_account')  # New field for specific sender account

            if tracking_code:
                queryset = queryset.filter(tracking_code=tracking_code)
                if not queryset.exists():
                    messages.append("No transactions found with the specified tracking code.")

            if min_amount:
                queryset = queryset.filter(amount__gte=min_amount)
                if not queryset.exists():
                    messages.append(f"No transactions found with an amount greater than or equal to {min_amount}.")

            if max_amount:
                queryset = queryset.filter(amount__lte=max_amount)
                if not queryset.exists():
                    messages.append(f"No transactions found with an amount less than or equal to {max_amount}.")

            if exact_amount:
                queryset = queryset.filter(amount=exact_amount)
                if not queryset.exists():
                    messages.append(f"No transactions found with an exact amount of {exact_amount}.")

            if receiver_account:
                queryset = queryset.filter(receiver__account_number=receiver_account)
                if not queryset.exists():
                    messages.append(f"No transactions found with the specified receiver account number {receiver_account}.")

            # If a specific sender account ID is provided, filter the queryset
            if sender_account_id:
                # Ensure the provided sender account ID belongs to the customer
                if sender_accounts.filter(id=sender_account_id).exists():
                    queryset = queryset.filter(sender__id=sender_account_id)
                    if not queryset.exists():
                        messages.append("No transactions found with the specified sender account.")
                else:
                    return Response({"error": "The specified sender account does not belong to the customer."}, status=status.HTTP_400_BAD_REQUEST)

            if start_date or end_date:
                try:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
                    end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None

                    if start_date and end_date:
                        queryset = queryset.filter(timestamp__range=(start_date, end_date))
                        if not queryset.exists():
                            messages.append("No transactions found in the specified date range.")
                    elif start_date:
                        queryset = queryset.filter(timestamp__gte=start_date)
                        if not queryset.exists():
                            messages.append("No transactions found after the specified start date.")
                    elif end_date:
                        queryset = queryset.filter(timestamp__lte=end_date)
                        if not queryset.exists():
                            messages.append("No transactions found before the specified end date.")
                except ValueError:
                    return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the queryset is empty after filtering
        if not queryset.exists():
            return Response({"message": "No transactions found matching the provided criteria.", "details": messages}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the final queryset
        serializer = TransactionSerializer(queryset, many=True)
        
        return Response({
            "message": "Transactions retrieved successfully.",
            "transactions": serializer.data
        }, status=status.HTTP_200_OK)
