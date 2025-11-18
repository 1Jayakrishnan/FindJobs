from django.shortcuts import render, get_object_or_404
from .serializers import JobPostSerialization, CompanySerializer, EventSerialization
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from employeeApp.models import JobPostModel, CompanyModel, EventsModel, EventsImages
from accountApp.models import User
import jwt, datetime
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

# Post Jobs
class Posting(APIView):
    permission_classes = [IsAuthenticated]  # Only logged-in users can post jobs

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id  # Attach logged-in user's ID automatically

        # print(data['user'])

        serializer = JobPostSerialization(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# Retrieve all posted job to see admin
class ViewPostedJobsForAdmin(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        jobs = JobPostModel.objects.all()
        serializer = JobPostSerialization(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# For GET or DELETE or UPDATE a single job post by ID
class JobDetail(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request, id):
        job = get_object_or_404(JobPostModel, id=id)
        serializer = JobPostSerialization(job)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, id):
        job = get_object_or_404(JobPostModel, id=id)
        if job.user != request.user:
            return Response("You don't have access to modify this job post!")
        else:
            obj = JobPostSerialization(
                instance=job, # the record to update
                data=request.data, # incoming new values
                partial = True
            )
            if obj.is_valid():
                obj.save()
                return Response("Data updates successfully!")
            else:
                return Response("Failed to update your Data!")

    def delete(self, request, id):
        job = get_object_or_404(JobPostModel, id=id)
        if not job:
            return Response({'error': 'Job post not found'}, status=status.HTTP_404_NOT_FOUND)
        if job.user != request.user:
            return Response("You are not allowed to delete this post")
        job.delete()
        return Response({'message':'Job post deleted successfully'}, status=status.HTTP_200_OK)

# View logged in employee posted jobs
class MyPostedJobs(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        jobs = JobPostModel.objects.filter(user=user)
        serializer = JobPostSerialization(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# company profile
class CompanyProfilePosting(APIView):
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":"success",
                "message":"Company profile created!",
                "data":serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "failed",
            "message": "Company profile if failed to create!",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class AllCompanyProfileFetching(APIView):
    def get(self, request):
        company_profiles = CompanyModel.objects.all()
        serializer = CompanySerializer(company_profiles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OneCompanyProfileFetching(APIView):
    def get(self, request, id):
        company_profile = get_object_or_404(CompanyModel, id=id)
        serializer = CompanySerializer(company_profile)
        return Response({
            "status":"success",
            "message":f"`{company_profile.name}` profile fetched successfully!",
            "data":serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, id):
        company_profile = CompanyModel.objects.get(id=id)
        serializer = CompanySerializer(
            instance=company_profile,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":"success",
                "message":"Company profile updated successfully!",
                "data":serializer.data
            }, status=status.HTTP_200_OK)

    def delete(self, request, id):
        company_profile = CompanyModel.objects.get(id=id)
        if company_profile:
            company_profile.delete()
            return Response({
                "status":"success",
                "message":f"company profile, `{company_profile.name}` deleted!",
            }, status=status.HTTP_200_OK)
        return Response({
            "status":"failed",
            "message":"company profile failed to delete!"
        }, status=status.HTTP_400_BAD_REQUEST)


class EventsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, MultiPartParser]
    # get all events
    def get(self, request):
        events = EventsModel.objects.all()
        serializer = EventSerialization(events, many=True)
        return Response({
            "status":"success",
            "message":"Data fetched successfully!",
            "data":serializer.data
        }, status=status.HTTP_200_OK)

    # create new event
    def post(self, request):
        # pass context={'request': request} to get the user id,
        # create() inside the serialization can use user = self.context['request'].user to get the id
        serializer = EventSerialization(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":"success",
                "message":"New event created successfully!",
                "data":serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status":"failed",
            "message":"failed to create new event",
            "errors":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# path for deleting the specified event(will delete including images)
class DeleteAnyEventAPI(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, id):
        event_obj = get_object_or_404(EventsModel, id=id)
        if event_obj.user != request.user:
            return Response({
                "status":"failed",
                "message":"Only posted owner can delete this event"
            })
        else:
            if event_obj:
                event_obj.delete()
                return Response({
                    "status":"success",
                    "message":f"event id - {id} deleted successfully!"
                })
            return Response({
                "status":"failed",
                "message":f"event id - {id} is not found to delete!"
            })

# delete any image of a particular event id
class DeleteAnyImageOfEventAPI(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, img_id):
        img_obj = get_object_or_404(EventsImages, id=img_id)
        if img_obj.event.user != request.user:
            return Response({
                "status":"failed",
                "message":"Only owner can delete this image"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            if img_obj:
                img_obj.delete()
                return Response({
                    "status":"success",
                    "message":f"Image id {(img_id)} deleted from event"
                }, status=status.HTTP_200_OK)
            return Response({
                "status":"failed",
                "message":"Image or event trying to delete is invalid!"
            }, status=status.HTTP_404_NOT_FOUND)

# add image to an existing event
class AddImagesToExistingEventAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def patch(self, request, event_id):
        event = get_object_or_404(EventsModel, id=event_id)
        if event.user != request.user:
            return Response({
                "status":"failed",
                "message":"Only owner can add image to this event"
            }, status=status.HTTP_400_BAD_REQUEST)

        uploaded_images = request.FILES.getlist('event_image')
        for img in uploaded_images:
            EventsImages.objects.create(event=event, event_image=img)
        return Response({
            "status":"success",
            "message":f"{len(uploaded_images)} image(s) added to event id {event_id}"
        })

# fetch all events posted by owner
class MyPostedEvents(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        events = EventsModel.objects.filter(user=request.user)
        serializer = EventSerialization(events, many=True)
        if events.exists():
            return Response({
                "status":"success",
                "message":"fetched all events you posted!",
                "data":serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status":"failed",
            "message":"No events to fetch"
        }, status=status.HTTP_404_NOT_FOUND)


