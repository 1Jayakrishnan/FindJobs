from django.urls import path
from accountApp import views
from employeeApp.views import JobList

urlpatterns = [
    path('Registration/',views.Registration.as_view()),
    path('LoginView/',views.LoginView.as_view()),
    path('UserView/',views.UserView.as_view()),
    path('UserLogout/',views.UserLogout.as_view()),
    path('refresh/', views.RefreshTokenView.as_view()),

    path('Openings/', JobList.as_view())
]