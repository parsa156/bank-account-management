from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Employee, Manager, Boss
from .serializers import EmployeeSerializer, ManagerSerializer, BossSerializer

# Employee Views
class EmployeeListView(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

class EmployeeCreateView(APIView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailView(APIView):
    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def put(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Manager Views
class ManagerListView(APIView):
    def get(self, request):
        managers = Manager.objects.all()
        serializer = ManagerSerializer(managers, many=True)
        return Response(serializer.data)

class ManagerCreateView(APIView):
    def post(self, request):
        serializer = ManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManagerDetailView(APIView):
    def get(self, request, pk):
        manager = get_object_or_404(Manager, pk=pk)
        serializer = ManagerSerializer(manager)
        return Response(serializer.data)

    def put(self, request, pk):
        manager = get_object_or_404(Manager, pk=pk)
        serializer = ManagerSerializer(manager, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        manager = get_object_or_404(Manager, pk=pk)
        manager.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Boss Views
class BossListView(APIView):
    def get(self, request):
        bosses = Boss.objects.all()
        serializer = BossSerializer(bosses, many=True)
        return Response(serializer.data)

class BossCreateView(APIView):
    def post(self, request):
        serializer = BossSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BossDetailView(APIView):
    def get(self, request, pk):
        boss = get_object_or_404(Boss, pk=pk)
        serializer = BossSerializer(boss)
        return Response(serializer.data)

    def put(self, request, pk):
        boss = get_object_or_404(Boss, pk=pk)
        serializer = BossSerializer(boss, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        boss = get_object_or_404(Boss, pk=pk)
        boss.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
