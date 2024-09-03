from django.db import models
from django.core.validators import MinLengthValidator

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=20,validators=[MinLengthValidator(8)])
    
    def __str__(self):
         return f"{self.first_name} {self.last_name}"
