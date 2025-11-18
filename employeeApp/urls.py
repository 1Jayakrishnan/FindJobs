from django.urls import path, include
from . import views


urlpatterns = [
    path("Posting/", views.Posting.as_view()),
    path("JobList/", views.ViewPostedJobsForAdmin.as_view()),

    path("JobDetail/<int:id>/", views.JobDetail.as_view()),

    path("MyPostedJobs/", views.MyPostedJobs.as_view()),

    path("create-company-profile/", views.CompanyProfilePosting.as_view()),
    path("list-company-profile/", views.AllCompanyProfileFetching.as_view()),
    path("fetch-company-profile/<int:id>/", views.OneCompanyProfileFetching.as_view()),

    path("events/", views.EventsAPIView.as_view()),
    # path for adding images to an existing event
    path("events/<int:event_id>/add-images/", views.AddImagesToExistingEventAPI.as_view()),
    # path for deleting the specified event(will delete including images)
    path("events/<int:id>/", views.DeleteAnyEventAPI.as_view()),
    # path for delete any image of a particular event id
    # path("event/<int:event_id>/image/<int:img_id>/", views.DeleteAnyImageOfEventAPI.as_view()),
    path("event/image/<int:img_id>/", views.DeleteAnyImageOfEventAPI.as_view()),
    # path for fetching my posted events
    path("my-events/",views.MyPostedEvents.as_view()),
]