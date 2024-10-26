from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Employee, Manager, Boss, PendingEmployee
from .serializers import EmployeeSerializer, ManagerSerializer, PendingEmployeeSerializer
from django.shortcuts import get_object_or_404

# Boss Creates Manager
class BossCreateManagerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'Boss':
            return Response({'error': 'Only d Boss can create a Manager.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Employee Signup
class EmployeeSignupView(APIView):
    def post(self, request):
        serializer = PendingEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save to the pending table
            return Response({'detail': 'Employee submitted for approval.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Manager and Boss approve or delete pending employees
class PendingEmployeeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'boss') and not hasattr(request.user, 'manager'):
            return Response({'error': 'Only Managers or Bosses can view pending employees.'}, status=status.HTTP_403_FORBIDDEN)
        pending_employees = PendingEmployee.objects.filter(is_accepted=False)
        serializer = PendingEmployeeSerializer(pending_employees, many=True)
        return Response(serializer.data)

class ApproveEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        if not hasattr(request.user, 'boss') and not hasattr(request.user, 'manager'):
            return Response({'error': 'Only Managers or Bosses can approve employees.'}, status=status.HTTP_403_FORBIDDEN)
        pending_employee = get_object_or_404(PendingEmployee, pk=pk)
        data = {
            'first_name': pending_employee.first_name,
            'last_name': pending_employee.last_name,
            'username': pending_employee.username,
            'code_meli': pending_employee.code_meli,
            'email': pending_employee.email,
            'bank': request.user.bank,
            'job_title': pending_employee.job_title,
            'hire_date': pending_employee.hire_date
        }
        employee_serializer = EmployeeSerializer(data=data)
        if employee_serializer.is_valid():
            employee_serializer.save()
            pending_employee.is_accepted = True
            pending_employee.save()
            return Response({'detail': 'Employee approved and added to employees.'}, status=status.HTTP_201_CREATED)
        return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeletePendingEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        if not hasattr(request.user, 'boss') and not hasattr(request.user, 'manager'):
            return Response({'error': 'Only Managers or Bosses can delete pending employees.'}, status=status.HTTP_403_FORBIDDEN)
        pending_employee = get_object_or_404(PendingEmployee, pk=pk)
        pending_employee.delete()
        return Response({'detail': 'Pending employee deleted.'}, status=status.HTTP_204_NO_CONTENT)
#Login
class CustomLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Try to find the user in Boss, Manager, or Employee tables
        user = None
        role = None

        try:
            user = Boss.objects.get(username=username)
            role = 'Boss'
        except Boss.DoesNotExist:
            try:
                user = Manager.objects.get(username=username)
                role = 'Manager'
            except Manager.DoesNotExist:
                try:
                    user = Employee.objects.get(username=username)
                    role = 'Employee'
                except Employee.DoesNotExist:
                    return Response({'error': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check the password manually
        if user and check_password(password, user.password):
            refresh = RefreshToken.for_user(user)
            
            # Return JWT tokens for the authenticated user
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': role
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)
        
# Boss dashboard: view all managers and employees
class BossDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'boss'):
            return Response({'error': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)

        managers = Manager.objects.filter(bank=request.user.bank).order_by('department_id')
        employees = Employee.objects.filter(bank=request.user.bank).order_by('department_id')

        manager_data = ManagerSerializer(managers, many=True).data
        employee_data = EmployeeSerializer(employees, many=True).data

        return Response({'managers': manager_data, 'employees': employee_data}, status=status.HTTP_200_OK)

# Manager dashboard: view all employees
class ManagerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'manager'):
            return Response({'error': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)

        employees = Employee.objects.filter(bank=request.user.bank).order_by('department_id')
        employee_data = EmployeeSerializer(employees, many=True).data
        return Response({'employees': employee_data}, status=status.HTTP_200_OK)

# Employee dashboard
class EmployeeDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'employee'):
            return Response({'error': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Only employees-related data can be shown here
        return Response({'detail': 'Employee dashboard content'}, status=status.HTTP_200_OK)

