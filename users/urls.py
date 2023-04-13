from django.urls import path
from . import views

urlpatterns = [
    path("me/", views.Me.as_view()),
    path("me/feedlike/", views.FeedLikes.as_view()),
    path("me/commentlike/", views.CommentLikes.as_view()),
    # path("@<str:username>/", views.UserDetail.as_view()),
    path("login/", views.LogIn.as_view()),
    path("checkID/", views.CheckID.as_view()),
    path("signup/", views.SignUp.as_view()),
    path("find/id/", views.FindId.as_view()),
    path("find/password/", views.FindPassword.as_view()),
    path("changepassword/", views.ChangePassword.as_view()),
    path("new-password/", views.NewPassword.as_view()),
]
