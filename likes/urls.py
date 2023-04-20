from rest_framework.urls import path
from . import views

urlpatterns = [
    path("feedlike/<int:pk>", views.FeedLikes.as_view()),
    path("commentlike/<int:pk>", views.CommentLikes.as_view()),
    path("recommentlike/<int:pk>", views.ReCommentLikes.as_view()),
]
