from enum import auto
from django.db import models
from django.forms import CharField, DateTimeField

# Create your models here.
# Buffer

class Contact(models.Model):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    description = models.CharField(max_length=3000, blank=False, null=False)

    