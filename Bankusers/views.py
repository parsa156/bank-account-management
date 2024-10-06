from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from .models import Employee, Manager, Boss
from .serializers import EmployeeSerializer, ManagerSerializer, BossSerializer, EmployeeSignUpSerializer

# Login view for Boss and Manager
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = Boss.objects.get(username=username)  # Change to Manager as needed
            if check_password(password, user.password):
                return Response({"message": "Login successful", "role": "boss"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        except Boss.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# Employee registration view
class EmployeeCreateView(APIView):
    def post(self, request):
        serializer = EmployeeSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Manager approval view for employees
class WaitingEmployeeListView(APIView):
    def get(self, request):
        # Only managers can see waiting employees
        waiting_employees = Employee.objects.filter(is_approved=False)  # Assuming you add an 'is_approved' field
        serializer = EmployeeSerializer(waiting_employees, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        # Manager approves or rejects the employee
        employee = get_object_or_404(Employee, pk=pk)
        action = request.data.get('action')  # 'approve' or 'reject'

        if action == 'approve':
            employee.is_approved = True
            employee.save()
            return Response({"message": "Employee approved"}, status=status.HTTP_200_OK)
        elif action == 'reject':
            employee.delete()
            return Response({"message": "Employee rejected"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
