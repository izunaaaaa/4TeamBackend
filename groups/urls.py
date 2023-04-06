from rest_framework.urls import path
from . import views

urlpatterns = [
    path("", views.Groups.as_view()),
]
