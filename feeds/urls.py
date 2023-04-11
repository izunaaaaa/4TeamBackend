from django.urls import path
from . import views

urlpatterns = [
    path("", views.Feeds.as_view()),
    path("<int:pk>", views.FeedDetail.as_view()),
    path("toplike", views.TopLikeView.as_view()),
]
