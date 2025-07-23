from django.shortcuts import render
from .serializers import JobPostSerialization
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from employeeApp.models import JobPostModel
from accountApp.models import User
import jwt, datetime

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

# Retrieve all posted job
class JobList(APIView):
    def get(self, request):
        jobs = JobPostModel.objects.all()
        serializer = JobPostSerialization(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# For GET or DELETE a single job post by ID

class JobDetail(APIView):
    def get(self, request, id):
        job = JobPostModel.objects.get(id=id)
        serializer = JobPostSerialization(job)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        job = JobPostModel.objects.get(id=id)
        obj = JobPostSerialization(
            instance=job, # the record to update
            data=request.data # incoming new values
        )
        if obj.is_valid():
            obj.save()
            return Response("Data updates successfully!")
        else:
            return Response("Failed to update your Data!")

    def delete(self, request, id):
        job = JobPostModel.objects.filter(id=id)
        if not job:
            return Response({'error': 'Job post not found'}, status=status.HTTP_404_NOT_FOUND)
        job.delete()
        return Response({'message':'Job post deleted successfully'}, status=status.HTTP_200_OK)
    
# View loggined employee posted jobs
class MyPostedJobs(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        jobs = JobPostModel.objects.filter(user=user)
        serializer = JobPostSerialization(jobs, many=True)
        return Response(serializer.data)