from django.db import models
from bank.models import Bank
from django.core.exceptions import ValidationError


class Person(models.Model):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)  # Username added
    code_meli = models.CharField(max_length=10, unique=True, blank=False, null=False)  # National ID (code meli) added
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Employee(Person):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='employees')
    job_title = models.CharField(max_length=50)
    hire_date = models.DateField()

class Manager(Person):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='managers')
    department_location = models.CharField(max_length=100)

class Boss(Person):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='bosses')
    headquarters_location = models.CharField(max_length=200)
