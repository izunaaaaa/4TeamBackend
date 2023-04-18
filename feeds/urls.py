from django.urls import path
from . import views

urlpatterns = [
    path("", views.Feeds.as_view()),  # 모든 게시글 보여주기, 게시글 업로드
    path("<int:pk>/", views.FeedDetail.as_view()),  # 게시글 디테일 / 게시글 수정 / 삭제
    path("group/category/", views.GroupFeedCategory.as_view()),
    path("toplike/", views.TopLikeView.as_view()),
    # path("group/", views.GroupFeeds.as_view()),
]
