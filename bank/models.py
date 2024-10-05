from django.db import models

class Bank(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=15 , blank=True , null=True)
    account_number_format = models.CharField(max_length=16, blank=False, null=False,default="xxxxxxxxxxxxxxxxxx")  # Example: '1234xxxx5678xxxx'
    
    def __str__(self):
        return self.name 