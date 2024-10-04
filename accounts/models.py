from django.db import models
from customers.models import Customer
from bank.models import Bank
import random

class BankAccount(models.Model):
    customer = models.ForeignKey(Customer, related_name='accounts', on_delete=models.CASCADE, blank=False, null=False)
    bank = models.ForeignKey(Bank, related_name='accounts', on_delete=models.CASCADE, blank=False, null=False)
    account_number = models.CharField(max_length=30, unique=True,  blank=False, null=False)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    transaction_password = models.CharField(max_length=4, blank=False, null=False)

    
    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"
    
    
    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    
    def generate_account_number(self):
        # Get format from the bank's account_number_format
        format_template = self.bank.account_number_format

        account_number = ''
        for char in format_template:
            if char == 'x':  # Replace 'x' with a random digit
                account_number += str(random.randint(0, 9))
            else:
                account_number += char
        return account_number
   
