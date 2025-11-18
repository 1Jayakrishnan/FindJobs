from rest_framework import serializers
from .models import JobPostModel, CompanyModel, EventsModel, EventsImages


class JobPostSerialization(serializers.ModelSerializer):
    class Meta:
        model = JobPostModel
        fields = "__all__"

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = "__all__"

class EventImageSerialization(serializers.ModelSerializer):
    class Meta:
        model = EventsImages
        fields = "__all__"

class EventSerialization(serializers.ModelSerializer):
    images = EventImageSerialization(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child = serializers.ImageField(max_length=10000, allow_empty_file=False, use_url=False),
        write_only=True
    )
    class Meta:
        model = EventsModel
        fields = ['id','description', 'images', 'uploaded_images']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')
        # take the logged-in user from the context
        user = self.context['request'].user
        event = EventsModel.objects.create(user=user,**validated_data)
        for img in uploaded_images:
            EventsImages.objects.create(event=event, event_image=img)
        return event