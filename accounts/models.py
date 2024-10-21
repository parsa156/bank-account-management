from django.db import models
from customers.models import Customer
from bank.models import Bank
import random,string
from django.contrib.auth.hashers import make_password, check_password
class BankAccount(models.Model):
    customer = models.ForeignKey(Customer, related_name='accounts', on_delete=models.CASCADE, blank=False, null=False)
    bank = models.ForeignKey(Bank, related_name='accounts', on_delete=models.CASCADE, blank=False, null=False)
    account_number = models.CharField(max_length=30, unique=True,  blank=False, null=False)
    balance = models.PositiveIntegerField(default=0)
    transaction_password = models.CharField(max_length=4, blank=False, null=False,default='0000')

    
    def __str__(self):
        return f"{self.bank} - {self.account_number}"
    
    
    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_unique_account_number()  # Ensure uniqueness
        if not self.transaction_password.startswith('pbkdf2_'):
            self.transaction_password = make_password(self.transaction_password)  
        super().save(*args, **kwargs)
    
    def check_transaction_password(self, password):
        return check_password(password, self.transaction_password)
    
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
    def generate_unique_account_number(self):
        # Retry until a unique account number is generated
        while True:
            account_number = self.generate_account_number()
            if not BankAccount.objects.filter(account_number=account_number).exists():
                return account_number
   
class Transaction(models.Model):
    sender = models.ForeignKey(BankAccount, related_name="sent_transactions", on_delete=models.CASCADE)
    receiver = models.ForeignKey(BankAccount, related_name="received_transactions", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tracking_code = models.CharField(max_length=15, unique=True, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically save the date and time of the transaction

    def generate_tracking_code(self):
        return ''.join(random.choices(string.ascii_letters + string.digits + '@#$', k=15))

    def generate_unique_tracking_code(self):
        while True:
            tracking_code = self.generate_tracking_code()
            if not Transaction.objects.filter(tracking_code=tracking_code).exists():
                return tracking_code

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = self.generate_unique_tracking_code()
        super().save(*args, **kwargs)