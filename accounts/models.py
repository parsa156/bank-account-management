from django.db import models
from customers.models import Customer

class Bank(models.Model):
    name = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15 , blank=True , null=True)

    def __str__(self):
        return self.name 
class BankAccount(models.Model):
    customer = models.ForeignKey(Customer, related_name='accounts', on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, related_name='accounts', on_delete=models.CASCADE, default=1)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=30, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"
   
