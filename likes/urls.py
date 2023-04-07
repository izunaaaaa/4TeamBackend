from rest_framework.urls import path
from . import views

urlpatterns = [
    path("feedlike", views.FeedLikes.as_view()),
    path("commentlike", views.CommentLikes.as_view()),
]
