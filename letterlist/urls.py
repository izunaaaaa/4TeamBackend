from rest_framework.urls import path
from . import views

urlpatterns = [
    path("me/", views.ChattingList.as_view()),  # 내 채팅방 목록 ( GET )
    path("<int:pk>/", views.ChattingRoom.as_view()),  # 채팅 내역 목록 ( GET )
    path("message/", views.MessageSend.as_view()),  # 채팅 post
    path("message/<int:pk>/", views.MessageDelete.as_view()),  # 채팅  delete
]
