from django.urls import path
from .views import BankListView, BankCreateView, BankDetailView

urlpatterns = [
    path('', BankListView.as_view(), name='bank-list'),           # GET all banks
    path('create/', BankCreateView.as_view(), name='bank-create'),  # POST to create a bank
    path('<int:pk>/', BankDetailView.as_view(), name='bank-detail'),  # GET, PUT, DELETE a bank
]
