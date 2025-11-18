from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime
from employeeApp.models import EventsModel

# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('jobseeker', 'Jobseeker'),
        ('employee', 'Employee')
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default="jobseeker")
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, null=True, default="1234567890")
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class EmailOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.otp_expires_at:
            self.otp_expires_at = timezone.now() + datetime.timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.created_at + datetime.timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"

class CommentsModel(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    event_id = models.ForeignKey(EventsModel, on_delete=models.CASCADE, related_name="event_comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
