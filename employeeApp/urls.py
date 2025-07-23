from django.urls import path
from . import views

urlpatterns = [

    path("Posting/", views.Posting.as_view()),
    path("JobList/", views.JobList.as_view()),
    path("JobDetail/<int:id>/", views.JobDetail.as_view()),

    path("MyPostedJobs/", views.MyPostedJobs.as_view())
]