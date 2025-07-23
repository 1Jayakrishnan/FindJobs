from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('jobseeker', 'Jobseeker'),
        ('employee', 'Employee')
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default="jobseeker")
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
