from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    Email = models.EmailField(max_length=200)
    code_meli= models.CharField(max_length= 10)
    Pasword = models.CharField(max_length=20)
    