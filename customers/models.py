from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100, editable=False, blank=False, null=False)
    last_name = models.CharField(max_length=100, editable=False, blank=False, null=False)
    email = models.EmailField(unique=True, editable=False, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
         return f"{self.first_name} {self.last_name}"
