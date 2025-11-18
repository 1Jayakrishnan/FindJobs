from rest_framework import serializers
from accountApp.models import User, EmailOTP, CommentsModel

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

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsModel
        fields = "__all__"
        read_only_fields = ['user_id', 'event_id', 'created_at']