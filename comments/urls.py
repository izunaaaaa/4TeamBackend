from rest_framework.urls import path
from . import views

urlpatterns = [
    path("", views.Comments.as_view()),
    path("<int:pk>", views.CommentDetail.as_view()),
]
