from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from bank.models import Bank

class PersonManager(BaseUserManager):
    def create_user(self, username, password=None, role=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        if role:
            extra_fields['role'] = role
        else:
            raise ValueError('User role must be set')  # Ensure role is provided
        
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, role='Boss', **extra_fields)
class Person(AbstractBaseUser):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    code_meli = models.CharField(max_length=10, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=128, blank=False, null=False)
    is_staff = models.BooleanField(default=False)
    ROLE_CHOICES = (
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
        ('Boss', 'Boss'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Employee')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'code_meli']

    objects = PersonManager()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Employee(Person):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='employees')
    job_title = models.CharField(max_length=50)
    hire_date = models.DateField()
    department = models.CharField(max_length=50)
    def save(self, *args, **kwargs):
        self.role = 'Employee'  
        super().save(*args, **kwargs)

class Manager(Person):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='managers')
    department_location = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    def save(self, *args, **kwargs):
        self.role = 'Manager'  
        super().save(*args, **kwargs)

class Boss(Person):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='bosses')
    headquarters_location = models.CharField(max_length=200)

class PendingEmployee(models.Model):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    code_meli = models.CharField(max_length=10, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    department_id = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    hire_date = models.DateField()
    is_accepted = models.BooleanField(default=False)
