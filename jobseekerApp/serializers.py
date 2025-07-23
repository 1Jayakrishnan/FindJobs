from rest_framework import serializers
from .models import UserProfileModel

class UserProfileModelSerialization(serializers.ModelSerializer):
    class Meta:
        model = UserProfileModel
        fields = "__all__"
