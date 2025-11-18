from django.urls import path
from accountApp import views
from employeeApp.views import ViewPostedJobsForAdmin

urlpatterns = [
    path('registration/',views.Registration.as_view(), name='registration'),
    path('login/',views.LoginView.as_view(), name='login'),
    path('userview/',views.UserView.as_view(), name='userview'),
    path('logout/',views.UserLogout.as_view(), name='logout'),
    path('refresh/', views.RefreshTokenView.as_view(), name='refresh'),

    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),

    path('posted-jobs/', ViewPostedJobsForAdmin.as_view(), name='posted-jobs'),
    # path for liking and unliking an event
    path("event/<int:event_id>/like/", views.LikeEventsAPI.as_view(), name='like-events'),
    # path for commenting under the events
    path('event/<int:event_id>/comments/', views.CommentsAPI.as_view(), name='comment-events'),
    # path for updating comments and deleting comments
    path('event/comments/<int:comment_id>/', views.ModifyComments.as_view(), name='edit-comments'),
]