from django.db import models
from employeeApp.models import JobPostModel
from django.conf import settings

# Create your models here.

class UserProfileModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="userprofilemodel")
    # jobseeker information
    FirstName = models.CharField(max_length=20, null=True, blank=True)
    LastName = models.CharField(max_length=20, null=True, blank=True)
    Gender = models.CharField(max_length=20, null=True, blank=True)
    Age = models.CharField(max_length=20, null=True, blank=True)
    Email = models.EmailField(max_length=20, null=True, blank=True)
    Phone = models.CharField(max_length=20, null=True, blank=True)
    Address = models.CharField(max_length=20, null=True, blank=True)
    ProfileImage = models.ImageField(upload_to="Jobseeker Profiles",null=True, blank=True)
    Aboutme = models.TextField(null=True, blank=True)
    # jobseeker educational information
    Degree = models.CharField(max_length=20, null=True, blank=True, default="")
    Stream = models.CharField(max_length=20, null=True, blank=True, default="")
    Institution = models.CharField(max_length=20, null=True, blank=True, default="")
    CollegeName = models.CharField(max_length=20, null=True, blank=True, default="")
    Start_year = models.CharField(null=True, blank=True, default="")
    End_year = models.CharField(null=True, blank=True, default="")
    CGPA = models.CharField(max_length=20, null=True, blank=True, default="")
    # resume and links
    Resume = models.FileField(upload_to="resumes/", null=True, blank=True)
    LinkdIn_url = models.URLField(max_length=200, null=True, blank=True)
    Portfolio_link = models.URLField(max_length=200, null=True, blank=True)

class JobApplicationModel(models.Model):
    job = models.ForeignKey(JobPostModel, on_delete=models.CASCADE, related_name="job_applications")
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applicants")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    resume = models.FileField(upload_to="applicant_resumes/", null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)



