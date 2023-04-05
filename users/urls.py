from django.urls import path
from . import views

urlpatterns = [
    path("me/", views.Me.as_view()),
    path("@<str:username>/", views.UserDetail.as_view()),
]
