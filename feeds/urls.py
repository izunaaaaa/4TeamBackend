from django.urls import path
from . import views

urlpatterns = [
    path("all", views.Feeds.as_view()),
    path("all/<int:pk>", views.FeedDetail.as_view()),
    path("<int:group_pk>", views.GroupFeeds.as_view()),
    path("<int:group_pk>/<int:category_pk>", views.GroupFeedCategory.as_view()),
    path("<int:group_pk>/<int:category_pk>/<int:pk>", views.GroupFeedDetail.as_view()),
    path("toplike", views.TopLikeView.as_view()),
]
