from django.db import models

class Bank(models.Model):
    name = models.CharField(max_length=100, unique=True, editable=False, blank=False, null=False)
    phone_number = models.CharField(max_length=15 , blank=True , null=True)

    def __str__(self):
        return self.name 