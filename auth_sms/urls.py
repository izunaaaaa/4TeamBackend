from rest_framework.urls import path
from . import views

urlpatterns = [
    path("send", views.SmsSend.as_view()),
    path("check", views.CheckNumber.as_view()),
]
