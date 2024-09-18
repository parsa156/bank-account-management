from django.db import models
from customers.models import Customer
from bank.models import Bank

class BankAccount(models.Model):
    customer = models.ForeignKey(Customer, related_name='accounts', on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, related_name='accounts', on_delete=models.CASCADE)
    account_number = models.CharField(max_length=30, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"
   
