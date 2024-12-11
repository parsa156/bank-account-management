from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from bank.models import Bank

class PersonManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, code_meli, password=None,role=None):
        if not username or not email or not first_name or not last_name or not code_meli:
            raise ValueError("All fields must be provided")
        if not password or len(password) < 8:  # Ensure password is provided and has at least 8 characters
            raise ValueError("A password must be provided and be at least 8 characters long")
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            code_meli=code_meli,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, code_meli, password=None, bank=None, **extra_fields):
        return self.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            code_meli=code_meli,
            password=password,
            role='Boss',
            bank=bank,
            **extra_fields
        )
class Person(AbstractBaseUser):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    code_meli = models.CharField(max_length=10, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128, blank=False, null=False)
    ROLE_CHOICES = (
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
        ('Boss', 'Boss'),
        ('Customer','Customer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'code_meli']

    objects = PersonManager()
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Customer(Person):
    def save(self, *args, **kwargs):
        self.role = 'Customer'  
        super().save(*args, **kwargs)
    
class Employee(Person):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='employees')
    job_title = models.CharField(max_length=50)
    department_id = models.CharField(max_length=50, blank=True, null=True)  
    def save(self, *args, **kwargs):
        self.role = 'Employee'  
        super().save(*args, **kwargs)

class Manager(Person):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='managers')
    department_location = models.CharField(max_length=100)
    department_id = models.CharField(max_length=50, blank=True, null=True)  
    def save(self, *args, **kwargs):
        self.role = 'Manager'  
        super().save(*args, **kwargs)

class Boss(Person):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='bosses')
    headquarters_location = models.CharField(max_length=200)
    def save(self, *args, **kwargs):
        self.role = 'Boss'  
        super().save(*args, **kwargs)

class PendingEmployee(models.Model):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    code_meli = models.CharField(max_length=10, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    department_id = models.CharField(max_length=50, blank=True, null=True)
    job_title = models.CharField(max_length=50)
    is_accepted = models.BooleanField(default=False)
    password = models.CharField(max_length=128, blank=False, null=False,default="12345678")
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)

