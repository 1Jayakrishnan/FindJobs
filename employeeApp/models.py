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
    Location = models.CharField(max_length=200, null=True, blank=True, default='TVM')
    lastDate = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)


class CompanyModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)

    # meta info
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class EventsModel(models.Model):
    description = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_model")
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_events", blank=True)

    def __str__(self):
        return self.description

class EventsImages(models.Model):
    event = models.ForeignKey(EventsModel, on_delete=models.CASCADE, related_name="images")
    event_image = models.ImageField(upload_to="events/images/", null=True, blank=True)