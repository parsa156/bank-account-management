from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomerManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, code_meli, password=None):
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
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class Customer(AbstractBaseUser):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)  
    code_meli = models.CharField(max_length=10, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=20, blank=False, null=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'code_meli']

    objects = CustomerManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"













from django.db import models

class Customer(models.Model):
   
    
    def __str__(self):
         return f"{self.first_name} {self.last_name}"
