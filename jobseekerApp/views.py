from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfileModel, JobApplicationModel
from .serializers import UserProfileModelSerialization, JobApplicationModelSerialization
from rest_framework.permissions import IsAuthenticated, AllowAny
from employeeApp.models import JobPostModel
from employeeApp.serializers import JobPostSerialization
from django.db.models import Q
import datetime

class UserProfileCreateView(APIView):
    def post(self, request):
        serializer = UserProfileModelSerialization(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User profile created successfully",
                             "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve all jobs which is currently active and before the last date of application
class AvailableJobsForJobseekers(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        jobs = JobPostModel.objects.filter(is_active=True, lastDate__gt=datetime.datetime.now())
        serializer = JobPostSerialization(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobApplicantView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        job_serialization = JobApplicationModelSerialization(data=request.data)
        # get the loggined user id
        user = request.user

        if job_serialization.is_valid(raise_exception=True):
            # check if job already applied
            job = job_serialization.validated_data['job']

            # compares two User objects
            if job.user == user:
                return Response({
                    "status": "failed",
                    "message": "You cannot apply for this job since you posted it."
                }, status=status.HTTP_400_BAD_REQUEST)

            if JobApplicationModel.objects.filter(job=job, applicant=request.user).exists():
                return Response({
                    "message": "You have already applied for this job.",
                })
            # save with logged-in user
            application = job_serialization.save(applicant=user)
            # try:
            #     user_profile = UserProfileModel.objects.get(user=request.user)
            # except UserProfileModel.DoesNotExist:
            #     print("no profile to fetch")
            return Response({
                "status":"success",
                "message":"Job applied!",
                "data": JobApplicationModelSerialization(application).data,
            }, status=status.HTTP_200_OK)

class JobSearchAPIView(APIView):
    def get(self, request, format=None):
        query = request.query_params.get('search', None)
        jobs = JobPostModel.objects.all()
        if query:
            jobs = jobs.filter(
                Q(JobTitle__icontains=query) |
                Q(Description__icontains=query) |
                Q(Experience__icontains=query)
            )
        serializer = JobPostSerialization(jobs, many=True)
        return Response(serializer.data)

