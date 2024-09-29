from django.urls import path
from .views import BankAccountListView, BankAccountCreateView, BankAccountDetailView

urlpatterns = [
    path('', BankAccountListView.as_view(), name='bankaccount-list'),             # GET all accounts
    path('create/', BankAccountCreateView.as_view(), name='bankaccount-create'),    # POST to create an account
    path('ccounts/<int:pk>/', BankAccountDetailView.as_view(), name='bankaccount-detail'),   # GET, PUT, DELETE an account
]
