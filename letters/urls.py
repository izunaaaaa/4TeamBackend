from rest_framework.urls import path
from . import views

urlpatterns = [
    path("", views.Letters.as_view()),
]
