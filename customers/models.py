from django.db import models
from django.core.validators import MinLengthValidator

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=20,validators=[MinLengthValidator(8)])
    
    def __str__(Name):
         return f"{Name.first_name} {Name.last_name}"
