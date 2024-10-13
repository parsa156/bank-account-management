from django.urls import path
from .views import BossCreateManagerView, EmployeeSignupView, PendingEmployeeListView, ApproveEmployeeView, DeletePendingEmployeeView, CustomLoginView, ManagerDashboardView,BossDashboardView
urlpatterns = [
    path('boss/create-manager/', BossCreateManagerView.as_view(), name='boss-create-manager'),
    path('employee/signup/', EmployeeSignupView.as_view(), name='employee-signup'),
    path('pending-employees/', PendingEmployeeListView.as_view(), name='pending-employee-list'),
    path('pending-employees/<int:pk>/approve/', ApproveEmployeeView.as_view(), name='approve-employee'),
    path('pending-employees/<int:pk>/delete/', DeletePendingEmployeeView.as_view(), name='delete-pending-employee'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('manager/dashboard/', ManagerDashboardView.as_view(), name='manager-dashboard'),
    path('boss/dashboard/', BossDashboardView.as_view(), name='boss-dashboard'),
]