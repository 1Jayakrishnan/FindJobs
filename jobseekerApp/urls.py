from django.urls import path
from . import views

urlpatterns = [
    path('create-profile/', views.UserProfileCreateView.as_view(), name="create-profile"),
    path('view-jobs/', views.AvailableJobsForJobseekers.as_view(), name="view-available-jobs"),
    path('job-apply/', views.JobApplicantView.as_view(), name="job-apply"),
    path('jobs-search/', views.JobSearchAPIView.as_view(), name='job-search')
]
