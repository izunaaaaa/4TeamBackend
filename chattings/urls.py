from rest_framework.urls import path
from . import views

urlpatterns = [
    path("", views.ChattingRoomList.as_view()),
    path("<int:pk>/", views.ChattingRoom.as_view()),
    # path("<int:pk>/chatlist", views.ChattingList.as_view()),
]
