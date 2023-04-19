from rest_framework.urls import path
from . import views

urlpatterns = [
    path("", views.AllAccessInfo.as_view()),
    path("group/<int:group_pk>", views.AccessInfoDetail.as_view()),
    path("group/<int:group_pk>/<int:user_pk>", views.AccessInfoDetailUser.as_view()),
]
