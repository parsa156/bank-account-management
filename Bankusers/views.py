from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated , AllowAny
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Employee, Manager, Boss, PendingEmployee,Person , Customer
from .serializers import EmployeeSerializer, ManagerSerializer, PendingEmployeeSerializer, Customerserializers, BossSerializer
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
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Employee Signup
class EmployeeSignupView(APIView):
    def post(self, request):
        serializer = PendingEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save to the pending table
            return Response({'detail': 'Employee submitted for approval.'}, status=status.HTTP_200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Manager and Boss approve or delete pending employees
class PendingEmployeeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'Boss' and user.role !='Manager':
            return Response({'error': 'Only Managers or Bosses can view pending employees.'}, status=status.HTTP_403_FORBIDDEN)
        pending_employees = PendingEmployee.objects.filter(is_accepted=False)
        serializer = PendingEmployeeSerializer(pending_employees, many=True)
        return Response(serializer.data)

class ApproveEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        boss = Boss.objects.get(id=user.id)
        bank_id = boss.bank.id
        if user.role != 'Boss' and user.role !='Manager':
            return Response({'error': 'Only Managers or Bosses can approve employees.'}, status=status.HTTP_403_FORBIDDEN)
        pending_employee = get_object_or_404(PendingEmployee, pk=pk)
        data = {
            'first_name': pending_employee.first_name,
            'last_name': pending_employee.last_name,
            'username': pending_employee.username,
            'code_meli': pending_employee.code_meli,
            'email': pending_employee.email,
            'bank': bank_id,
            'job_title': pending_employee.job_title,
            'password':pending_employee.password
        }
        employee_serializer = EmployeeSerializer(data=data)
        if employee_serializer.is_valid():
            employee_serializer.save()
            pending_employee.is_accepted = True
            pending_employee.save()
            return Response({'detail': 'Employee approved and added to employees.'}, status=status.HTTP_200_OK)
        return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeletePendingEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        user = request.user
        if user.role != 'Boss' and user.role !='Manager':
            return Response({'error': 'Only Managers or Bosses can delete pending employees.'}, status=status.HTTP_403_FORBIDDEN)
        pending_employee = get_object_or_404(PendingEmployee, pk=pk)
        pending_employee.delete()
        return Response({'detail': 'Pending employee deleted.'}, status=status.HTTP_200_OK)
#Login
class CustomLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Try to find the user in Boss, Manager, or Employee tables
        user = None
        role = None

        if Person.objects.filter(username=username).exists():
            user = Person.objects.get(username=username)
        else:
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
        user = request.user
        if user.role != 'Boss':
            return Response({'error': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)
        boss = Boss.objects.get(id=user.id)
        managers = Manager.objects.filter(bank=boss.bank).order_by('department_id')
        employees = Employee.objects.filter(bank=boss.bank).order_by('department_id')
        #accounts = Customer.objects.filter(bank=boss.bank)

        manager_data = ManagerSerializer(managers, many=True).data
        employee_data = EmployeeSerializer(employees, many=True).data
        #customer_data = Customerserializers(customers,many=True).data

        return Response({'managers': manager_data, 'employees': employee_data}, status=status.HTTP_200_OK)

# Manager dashboard: view all employees
class ManagerDashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            if user.role !='Manager':
                return Response({'error': 'Access denied.'}, status=status.HTTP_403_FORBIDDEN)
            manager=Manager.objects.get(id=user.id)
            employee = Employee.objects.filter(bank=manager.bank ,department_id=manager.department_id)
            employee_data = EmployeeSerializer(employee, many=True).data
            return Response({'employees': employee_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CustomerSignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = Customerserializers(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user=request.user
        id = user.id
        role = user.role
        match role:
            case _ if role == 'Customers':
                customer = Customer.objects.get(id=id)
                serializer = Customerserializers(customer)
            case _ if role == 'Employee':
                employee = Employee.objects.get(id=id)
                serializer = EmployeeSerializer(employee)   
            case _ if role == 'Manager':
                manager = Manager.objects.get(id=id)
                serializer = ManagerSerializer(manager) 
            case _ if role == 'Boss':
                boss = Boss.objects.get(id=id)
                serializer = BossSerializer(boss)       
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        id = user.id
        role = user.role
        
        try:
            match role:
                case 'Customer':  # Make sure this matches your ROLE_CHOICES
                    customer = Customer.objects.get(id=id)
                    serializer = Customerserializers(customer, data=request.data, partial=True)
                case 'Employee':
                    employee = Employee.objects.get(id=id)
                    serializer = EmployeeSerializer(employee, data=request.data, partial=True)
                case 'Manager':
                    manager = Manager.objects.get(id=id)
                    serializer = ManagerSerializer(manager, data=request.data, partial=True)
                case 'Boss':
                    boss = Boss.objects.get(id=id)
                    serializer = BossSerializer(boss, data=request.data, partial=True)
                case _:
                    return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
                
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Person.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
