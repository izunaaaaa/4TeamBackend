from rest_framework.urls import path
from . import views

urlpatterns = [
    path("", views.AllAccessInfo.as_view()),
]
