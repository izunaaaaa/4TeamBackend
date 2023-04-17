from rest_framework.urls import path
from . import views

urlpatterns = [
    path("", views.Categories.as_view()),
    path("<int:group_pk>", views.GroupCategories.as_view()),
    path("<int:group_pk>/<int:pk>", views.GroupCategoryDetail.as_view()),
]
