from django.db import models

# Create your models here.

class UserProfileModel(models.Model):
    FullName = models.CharField(max_length=20, null=True, blank=True)
    Gender = models.CharField(max_length=20, null=True, blank=True)
    Age = models.CharField(max_length=20, null=True, blank=True)
    Email = models.CharField(max_length=20, null=True, blank=True)
    Phone = models.CharField(max_length=20, null=True, blank=True)
    Address = models.CharField(max_length=20, null=True, blank=True)
    ProfileImage = models.ImageField(upload_to="Jobseeker Profiles",null=True, blank=True)
    