from django.db import models
from django.conf import settings

# Create your models here.
class JobPostModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_posts")
    JobTitle = models.CharField(max_length=100, null=True, blank=True)
    Company = models.CharField(max_length=100, null=True, blank=True)
    Description = models.TextField()
    Vacancy = models.CharField(max_length=100, null=True, blank=True)
    Salary = models.CharField(max_length=20, null=True, blank=True)
    Experience = models.CharField(max_length=20, null=True, blank=True)