from django.urls import path
from .views import UserProfileCreateView

urlpatterns = [
    path('create-profile/', UserProfileCreateView.as_view()),
]
