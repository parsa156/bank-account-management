from django.urls import path
from .views import (
    EmployeeListView, EmployeeCreateView, EmployeeDetailView, 
    ManagerListView, ManagerCreateView, ManagerDetailView, 
    BossListView, BossCreateView, BossDetailView, 
    EmployeeApprovalListView, EmployeeApprovalView
)

urlpatterns = [
    # Employee routes
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),

    # Manager routes
    path('managers/', ManagerListView.as_view(), name='manager-list'),
    path('managers/create/', ManagerCreateView.as_view(), name='manager-create'),
    path('managers/<int:pk>/', ManagerDetailView.as_view(), name='manager-detail'),

    # Boss routes
    path('bosses/', BossListView.as_view(), name='boss-list'),
    path('bosses/create/', BossCreateView.as_view(), name='boss-create'),
    path('bosses/<int:pk>/', BossDetailView.as_view(), name='boss-detail'),

    # Employee approval routes
    path('employees/waiting/', EmployeeApprovalListView.as_view(), name='employee-waiting-list'),
    path('employees/approve/<int:pk>/', EmployeeApprovalView.as_view(), name='employee-approve'),
]
