from rest_framework.urls import path
from . import views

urlpatterns = [
    path("", views.Categories.as_view()),
    path("<int:group>", views.GroupCategories.as_view()),
    path("<int:group>/<int:pk>", views.GroupCategoryDetail.as_view()),
]
