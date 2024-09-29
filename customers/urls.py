from django.urls import path
from .views import CustomerListView, CustomerCreateView, CustomerDetailView

urlpatterns = [
    path('', CustomerListView.as_view(), name='customer-list'),             # GET all customers
    path('create/', CustomerCreateView.as_view(), name='customer-create'),    # POST to create a customer
    path('<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),   # GET, PUT, DELETE a customer
]
