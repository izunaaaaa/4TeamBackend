from django.urls import path
from . import views

urlpatterns = [
    path("", views.Recomment.as_view()),
]
