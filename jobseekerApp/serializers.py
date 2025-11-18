from rest_framework import serializers
from .models import UserProfileModel, JobApplicationModel
from accountApp.models import User
from accountApp.serializers import UserProfileSerializer

class UserProfileModelSerialization(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = "__all__"

class JobApplicantDetailsSerialization(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = ('FirstName', 'Gender', 'Email', 'Phone', 'Resume')

class JobApplicationModelSerialization(serializers.ModelSerializer):
    # applicant_profile = JobApplicantDetailsSerialization(
    #     source="applicant.applicant_profile",
    #     read_only=True
    # )
    class Meta:
        model = JobApplicationModel
        fields = "__all__"
        read_only_fields = ['applicant','applied_at']



