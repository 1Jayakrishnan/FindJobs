from rest_framework import serializers
from .models import JobPostModel


class JobPostSerialization(serializers.ModelSerializer):
    class Meta:
        model = JobPostModel
        fields = "__all__"