from rest_framework import serializers
from accountApp.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    confirmpassword = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            'id','user_type', 'name','phone','email','password','confirmpassword'
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmpassword']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirmpassword')  # Exclude from saving
        #Extract the password field from validated_data, if present
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance